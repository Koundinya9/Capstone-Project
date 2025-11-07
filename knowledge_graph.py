import networkx as nx
from typing import Dict, List, Any, Optional, Tuple
import json
from datetime import datetime
import plotly.graph_objects as go

class CompetitiveKnowledgeGraph:
    """
    Knowledge Graph for Competitive Intelligence Analysis.
    Tracks companies, relationships, attributes, and enables complex queries.
    """
    
    def __init__(self):
        self.graph = nx.MultiDiGraph()  # Directed graph with multiple edges
        self.entity_attributes = {}  # Store detailed attributes for entities
        self.relationship_history = []  # Track when relationships are added
        
    def add_company(self, company_name: str, attributes: Dict[str, Any] = None):
        """Add a company node to the knowledge graph."""
        if attributes is None:
            attributes = {}
        
        # Add timestamp
        attributes['added_at'] = datetime.now().isoformat()
        attributes['entity_type'] = 'company'
        
        self.graph.add_node(company_name, **attributes)
        self.entity_attributes[company_name] = attributes
        
    def add_relationship(self, source: str, target: str, relationship_type: str, 
                        attributes: Dict[str, Any] = None):
        """Add a relationship between two entities."""
        if attributes is None:
            attributes = {}
            
        attributes['relationship_type'] = relationship_type
        attributes['added_at'] = datetime.now().isoformat()
        
        self.graph.add_edge(source, target, **attributes)
        
        # Track relationship history
        self.relationship_history.append({
            'source': source,
            'target': target,
            'type': relationship_type,
            'timestamp': attributes['added_at']
        })
        
    def add_product(self, product_name: str, company: str, attributes: Dict[str, Any] = None):
        """Add a product and link it to a company."""
        if attributes is None:
            attributes = {}
            
        attributes['entity_type'] = 'product'
        attributes['added_at'] = datetime.now().isoformat()
        
        self.graph.add_node(product_name, **attributes)
        self.entity_attributes[product_name] = attributes
        
        # Link product to company
        self.add_relationship(company, product_name, 'produces', {
            'description': f'{company} produces {product_name}'
        })
        
    def add_market(self, market_name: str, attributes: Dict[str, Any] = None):
        """Add a market/industry segment."""
        if attributes is None:
            attributes = {}
            
        attributes['entity_type'] = 'market'
        attributes['added_at'] = datetime.now().isoformat()
        
        self.graph.add_node(market_name, **attributes)
        self.entity_attributes[market_name] = attributes
        
    def add_person(self, person_name: str, company: str, role: str, 
                   attributes: Dict[str, Any] = None):
        """Add a person (executive, founder, etc.) and link to company."""
        if attributes is None:
            attributes = {}
            
        attributes['entity_type'] = 'person'
        attributes['role'] = role
        attributes['added_at'] = datetime.now().isoformat()
        
        self.graph.add_node(person_name, **attributes)
        self.entity_attributes[person_name] = attributes
        
        # Link person to company
        self.add_relationship(person_name, company, 'works_at', {
            'role': role,
            'description': f'{person_name} is {role} at {company}'
        })
        
    def get_competitors(self, company: str) -> List[str]:
        """Get all competitors of a company."""
        competitors = []
        
        # Outgoing competitor relationships
        for target in self.graph.successors(company):
            edges = self.graph.get_edge_data(company, target)
            if edges:
                for edge_data in edges.values():
                    if edge_data.get('relationship_type') == 'competes_with':
                        competitors.append(target)
        
        # Incoming competitor relationships (bidirectional)
        for source in self.graph.predecessors(company):
            edges = self.graph.get_edge_data(source, company)
            if edges:
                for edge_data in edges.values():
                    if edge_data.get('relationship_type') == 'competes_with':
                        if source not in competitors:
                            competitors.append(source)
        
        return competitors
    
    def get_shared_markets(self, company1: str, company2: str) -> List[str]:
        """Find markets that both companies operate in."""
        markets1 = set()
        markets2 = set()
        
        # Get markets for company1
        for target in self.graph.successors(company1):
            if self.graph.nodes[target].get('entity_type') == 'market':
                markets1.add(target)
        
        # Get markets for company2
        for target in self.graph.successors(company2):
            if self.graph.nodes[target].get('entity_type') == 'market':
                markets2.add(target)
        
        return list(markets1.intersection(markets2))
    
    def get_company_products(self, company: str) -> List[str]:
        """Get all products of a company."""
        products = []
        
        for target in self.graph.successors(company):
            if self.graph.nodes[target].get('entity_type') == 'product':
                products.append(target)
        
        return products
    
    def get_company_leadership(self, company: str) -> List[Dict[str, str]]:
        """Get leadership team of a company."""
        leadership = []
        
        for source in self.graph.predecessors(company):
            if self.graph.nodes[source].get('entity_type') == 'person':
                person_data = self.graph.nodes[source]
                leadership.append({
                    'name': source,
                    'role': person_data.get('role', 'Unknown'),
                    'attributes': person_data
                })
        
        return leadership
    
    def find_competitive_threats(self, user_company: str, competitor: str) -> Dict[str, Any]:
        """Analyze competitive threats between user company and competitor."""
        threats = {
            'shared_markets': self.get_shared_markets(user_company, competitor),
            'competitor_advantages': [],
            'overlapping_products': [],
            'market_position': {}
        }
        
        # Get products
        user_products = set(self.get_company_products(user_company))
        competitor_products = set(self.get_company_products(competitor))
        
        # Check for product overlaps
        for user_prod in user_products:
            for comp_prod in competitor_products:
                # Check if products compete in same category
                user_attrs = self.graph.nodes[user_prod]
                comp_attrs = self.graph.nodes[comp_prod]
                
                if user_attrs.get('category') == comp_attrs.get('category'):
                    threats['overlapping_products'].append({
                        'user_product': user_prod,
                        'competitor_product': comp_prod,
                        'category': user_attrs.get('category')
                    })
        
        return threats
    
    def get_relationship_path(self, source: str, target: str, max_length: int = 3) -> List[List[str]]:
        """Find paths between two entities (useful for discovering indirect relationships)."""
        try:
            paths = []
            # Find all simple paths up to max_length
            for path in nx.all_simple_paths(self.graph, source, target, cutoff=max_length):
                paths.append(path)
            return paths
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return []
    
    def get_company_network(self, company: str, depth: int = 1) -> Dict[str, Any]:
        """Get the network of entities around a company up to specified depth."""
        network = {
            'company': company,
            'competitors': [],
            'products': [],
            'markets': [],
            'leadership': [],
            'relationships': []
        }
        
        # Get immediate connections
        for neighbor in self.graph.successors(company):
            node_type = self.graph.nodes[neighbor].get('entity_type')
            edges = self.graph.get_edge_data(company, neighbor)
            
            for edge_data in edges.values():
                rel_type = edge_data.get('relationship_type')
                
                if rel_type == 'competes_with':
                    network['competitors'].append(neighbor)
                elif node_type == 'product':
                    network['products'].append(neighbor)
                elif node_type == 'market':
                    network['markets'].append(neighbor)
                
                network['relationships'].append({
                    'from': company,
                    'to': neighbor,
                    'type': rel_type,
                    'attributes': edge_data
                })
        
        # Get incoming connections
        for neighbor in self.graph.predecessors(company):
            node_type = self.graph.nodes[neighbor].get('entity_type')
            
            if node_type == 'person':
                network['leadership'].append(neighbor)
            
            edges = self.graph.get_edge_data(neighbor, company)
            for edge_data in edges.values():
                network['relationships'].append({
                    'from': neighbor,
                    'to': company,
                    'type': edge_data.get('relationship_type'),
                    'attributes': edge_data
                })
        
        return network
    
    def query_entities_by_attribute(self, entity_type: str, attribute: str, 
                                   value: Any) -> List[str]:
        """Query entities by type and attribute value."""
        results = []
        
        for node, attrs in self.graph.nodes(data=True):
            if attrs.get('entity_type') == entity_type:
                if attrs.get(attribute) == value:
                    results.append(node)
        
        return results
    
    def get_market_landscape(self, market: str) -> Dict[str, Any]:
        """Get all companies operating in a specific market."""
        landscape = {
            'market': market,
            'companies': [],
            'market_attributes': self.graph.nodes[market] if market in self.graph else {}
        }
        
        # Find all companies that operate in this market
        for source in self.graph.predecessors(market):
            if self.graph.nodes[source].get('entity_type') == 'company':
                company_data = {
                    'name': source,
                    'attributes': self.graph.nodes[source],
                    'products_in_market': []
                }
                
                # Get products in this market
                for product in self.get_company_products(source):
                    product_markets = [t for t in self.graph.successors(product) 
                                     if self.graph.nodes[t].get('entity_type') == 'market']
                    if market in product_markets:
                        company_data['products_in_market'].append(product)
                
                landscape['companies'].append(company_data)
        
        return landscape
    
    def export_graph_data(self) -> Dict[str, Any]:
        """Export graph data for visualization or persistence."""
        return {
            'nodes': [
                {
                    'id': node,
                    'attributes': attrs
                }
                for node, attrs in self.graph.nodes(data=True)
            ],
            'edges': [
                {
                    'source': u,
                    'target': v,
                    'attributes': attrs
                }
                for u, v, attrs in self.graph.edges(data=True)
            ],
            'stats': {
                'total_nodes': self.graph.number_of_nodes(),
                'total_edges': self.graph.number_of_edges(),
                'companies': len([n for n, d in self.graph.nodes(data=True) 
                                if d.get('entity_type') == 'company']),
                'products': len([n for n, d in self.graph.nodes(data=True) 
                               if d.get('entity_type') == 'product']),
                'markets': len([n for n, d in self.graph.nodes(data=True) 
                              if d.get('entity_type') == 'market'])
            }
        }
    
    def parse_entity_extraction(self, extracted_text: str, user_company: str, competitor: str) -> None:
        """
        Parse the output from entity extraction task and populate the knowledge graph.
        
        Args:
            extracted_text (str): The structured text output from entity_extraction_task
            user_company (str): The name of the user's company
            competitor (str): The name of the competitor being analyzed
        """
        # Make sure the core companies exist first
        if not user_company in self.graph:
            self.add_company(user_company, {'is_user_company': True})
        if not competitor in self.graph:
            self.add_company(competitor, {'is_competitor': True})
            self.add_relationship(user_company, competitor, 'competes_with', {
                'identified_at': datetime.now().isoformat()
            })
        
        # Split the text into sections using a more robust method
        sections = {}
        current_section = None
        current_content = []
        
        # First, normalize the text to handle various formats
        lines = [line.strip() for line in extracted_text.split('\n') if line.strip()]
        section_markers = ['COMPANIES:', 'PRODUCTS:', 'MARKETS:', 'PEOPLE:', 'RELATIONSHIPS:']
        
        for line in lines:
            # Check if line is a section marker
            is_section = False
            for marker in section_markers:
                if line.upper().startswith(marker.upper()):
                    if current_section and current_content:
                        sections[current_section] = current_content
                    current_section = marker[:-1]  # Remove the colon
                    current_content = []
                    is_section = True
                    break
            
            # If not a section marker and we have a current section, add to content
            if not is_section and current_section:
                current_content.append(line)
        
        # Add the last section
        if current_section and current_content:
            sections[current_section] = current_content
        
        # Process each section with better error handling
        try:
            # Process COMPANIES section
            if 'COMPANIES' in sections:
                for line in sections['COMPANIES']:
                    try:
                        if not line.startswith('- '):
                            continue
                            
                        # Remove bullet point and split into name and attributes
                        line = line[2:].strip()
                        parts = line.split(':', 1)
                        
                        if len(parts) == 2:
                            company = parts[0].strip()
                            attrs_str = parts[1].strip()
                            
                            # Try to parse attributes, with fallback
                            try:
                                # First try to parse as a Python dict
                                attrs = eval('{' + attrs_str + '}')
                            except:
                                # If that fails, try to parse key=value pairs
                                attrs = {}
                                for pair in attrs_str.split(','):
                                    if '=' in pair:
                                        k, v = pair.split('=', 1)
                                        attrs[k.strip()] = v.strip()
                                    else:
                                        attrs['description'] = attrs_str.strip()
                            
                            # Only add if we don't already have this company
                            if company not in self.graph:
                                self.add_company(company, attrs)
                    except Exception as e:
                        print(f"Error processing company line: {line}. Error: {str(e)}")
                        continue
            
            # Process PRODUCTS section with improved attribute parsing
            if 'PRODUCTS' in sections:
                for line in sections['PRODUCTS']:
                    try:
                        if not line.startswith('- '):
                            continue
                            
                        line = line[2:].strip()
                        if ':' not in line:
                            continue
                            
                        product, attrs_str = line.split(':', 1)
                        product = product.strip()
                        
                        # Parse attributes more robustly
                        attrs = {}
                        company = None
                        
                        # Try different attribute formats
                        for attr in attrs_str.split(','):
                            attr = attr.strip()
                            if '=' in attr:
                                key, value = attr.split('=', 1)
                                key = key.strip()
                                value = value.strip()
                                if key == 'company':
                                    company = value
                                else:
                                    attrs[key] = value
                            else:
                                attrs['description'] = attr
                        
                        # If no company specified, try to infer from context
                        if not company and len(attrs_str.split()) >= 2:
                            # Look for company names in the attributes string
                            for potential_company in [competitor, user_company]:
                                if potential_company.lower() in attrs_str.lower():
                                    company = potential_company
                                    break
                        
                        if company:
                            self.add_product(product, company, attrs)
                    except Exception as e:
                        print(f"Error processing product line: {line}. Error: {str(e)}")
                        continue
            
            # Process MARKETS section with automatic relationships
            if 'MARKETS' in sections:
                for line in sections['MARKETS']:
                    try:
                        if not line.startswith('- '):
                            continue
                            
                        line = line[2:].strip()
                        if ':' not in line:
                            continue
                            
                        market, attrs_str = line.split(':', 1)
                        market = market.strip()
                        
                        # Parse attributes with fallback
                        try:
                            attrs = eval('{' + attrs_str.strip() + '}')
                        except:
                            attrs = {'description': attrs_str.strip()}
                        
                        # Add market if it doesn't exist
                        if market not in self.graph:
                            self.add_market(market, attrs)
                        
                        # Add relationships to companies
                        if 'companies' in attrs:
                            companies = attrs['companies']
                            if isinstance(companies, str):
                                companies = [c.strip() for c in companies.split(',')]
                            for company in companies:
                                if company in self.graph:
                                    self.add_relationship(company, market, 'operates_in')
                        else:
                            # Default to adding both user company and competitor
                            self.add_relationship(user_company, market, 'operates_in')
                            self.add_relationship(competitor, market, 'operates_in')
                    except Exception as e:
                        print(f"Error processing market line: {line}. Error: {str(e)}")
                        continue
            
            # Process PEOPLE section with role inference
            if 'PEOPLE' in sections:
                for line in sections['PEOPLE']:
                    try:
                        if not line.startswith('- '):
                            continue
                            
                        line = line[2:].strip()
                        if ':' not in line:
                            continue
                            
                        person, attrs_str = line.split(':', 1)
                        person = person.strip()
                        
                        # Initialize with defaults
                        attrs = {
                            'role': 'Unknown',
                            'company': None
                        }
                        
                        # Parse attributes
                        pairs = [pair.strip() for pair in attrs_str.split(',')]
                        for pair in pairs:
                            if '=' in pair:
                                key, value = pair.split('=', 1)
                                key = key.strip().lower()
                                value = value.strip()
                                
                                if key == 'company':
                                    attrs['company'] = value
                                elif key in ['role', 'position', 'title']:
                                    attrs['role'] = value
                        
                        # If company not specified, try to infer
                        if not attrs['company']:
                            if user_company.lower() in attrs_str.lower():
                                attrs['company'] = user_company
                            elif competitor.lower() in attrs_str.lower():
                                attrs['company'] = competitor
                        
                        if attrs['company']:
                            self.add_person(person, attrs['company'], attrs['role'])
                    except Exception as e:
                        print(f"Error processing person line: {line}. Error: {str(e)}")
                        continue
            
            # Process RELATIONSHIPS section with validation
            if 'RELATIONSHIPS' in sections:
                for line in sections['RELATIONSHIPS']:
                    try:
                        if not line.startswith('- '):
                            continue
                            
                        line = line[2:].strip()
                        if '->' not in line:
                            continue
                            
                        parts = line.split('->')
                        if len(parts) >= 3:
                            source = parts[0].strip()
                            rel_type = parts[1].strip()
                            target_part = parts[2]
                            
                            # Handle case where target has a description
                            target_parts = target_part.split(':', 1)
                            target = target_parts[0].strip()
                            description = target_parts[1].strip() if len(target_parts) > 1 else None
                            
                            # Only add relationship if both nodes exist
                            if source in self.graph and target in self.graph:
                                attrs = {}
                                if description:
                                    attrs['description'] = description
                                
                                self.add_relationship(source, target, rel_type, attrs)
                    except Exception as e:
                        print(f"Error processing relationship line: {line}. Error: {str(e)}")
                        continue
                        
        except Exception as e:
            print(f"Error during entity extraction: {str(e)}")
            raise

    def import_from_analysis(self, user_company: str, competitor: str, 
                           analysis_text: str) -> None:
        """
        Parse competitive intelligence analysis and populate knowledge graph.
        This is a smart parser that extracts entities and relationships.
        """
        # Add main companies
        self.add_company(user_company, {'is_user_company': True})
        self.add_company(competitor, {'is_competitor': True})
        
        # Add competitor relationship
        self.add_relationship(user_company, competitor, 'competes_with', {
            'description': f'{user_company} competes with {competitor}'
        })
        
        # Parse analysis text for entities (basic implementation)
        # In production, you'd use NER (Named Entity Recognition) or LLM extraction
        
        # Look for market mentions
        market_keywords = ['market', 'industry', 'segment', 'sector']
        for keyword in market_keywords:
            if keyword in analysis_text.lower():
                # Extract context around keyword
                # This is simplified - in production use more sophisticated NLP
                pass
        
    def get_graph_summary(self) -> str:
        """Get a text summary of the knowledge graph."""
        stats = self.export_graph_data()['stats']
        
        summary = f"""
**Knowledge Graph Summary**

- Total Entities: {stats['total_nodes']}
- Total Relationships: {stats['total_edges']}
- Companies: {stats['companies']}
- Products: {stats['products']}
- Markets: {stats['markets']}

**Top Companies by Connections:**
"""
        # Get companies with most connections
        companies = [(n, self.graph.degree(n)) for n, d in self.graph.nodes(data=True) 
                    if d.get('entity_type') == 'company']
        companies.sort(key=lambda x: x[1], reverse=True)
        
        for company, degree in companies[:5]:
            summary += f"\n- {company}: {degree} connections"
        
        return summary
    
    def visualize_graph(self, focus_company: Optional[str] = None, depth: int = 2):
        """Generate an interactive graph visualization using Plotly."""
        if self.graph.number_of_nodes() < 1:
            raise ValueError("Graph is empty - no nodes to visualize")
            
        # If focus company is provided, get subgraph centered on that company
        if focus_company and focus_company in self.graph:
            nodes_to_include = {focus_company}
            for _ in range(depth):
                for node in list(nodes_to_include):
                    nodes_to_include.update(self.graph.predecessors(node))
                    nodes_to_include.update(self.graph.successors(node))
            subgraph = self.graph.subgraph(nodes_to_include)
        else:
            subgraph = self.graph
            
        # Use spring layout with adjusted parameters for better spacing
        try:
            pos = nx.spring_layout(
                subgraph,
                k=2.0 / (self.graph.number_of_nodes() ** 0.5),  # Adaptive k based on graph size
                iterations=100,
                weight=None  # Ignore edge weights for layout
            )
        except Exception as e:
            # Fallback to basic layout if spring layout fails
            pos = {node: (idx % 3 - 1, idx // 3 - 1) for idx, node in enumerate(subgraph.nodes())}
        
        # Create edge traces - group by relationship type
        edge_traces = []
        relationship_types = set()
        for edge in subgraph.edges(data=True):
            relationship_types.add(edge[2].get('relationship_type', 'connected to'))
            
        edge_colors = {
            'competes_with': '#ff0000',  # Red
            'produces': '#00ff00',       # Green
            'operates_in': '#0000ff',    # Blue
            'works_at': '#ffff00',       # Yellow
            'connected to': '#888888'    # Gray
        }
        
        for rel_type in relationship_types:
            edge_x = []
            edge_y = []
            edge_text = []
            
            for edge in subgraph.edges(data=True):
                if edge[2].get('relationship_type', 'connected to') == rel_type:
                    x0, y0 = pos[edge[0]]
                    x1, y1 = pos[edge[1]]
                    edge_x.extend([x0, x1, None])
                    edge_y.extend([y0, y1, None])
                    edge_text.append(f"{edge[0]} {rel_type} {edge[1]}")
            
            if edge_x:  # Only add trace if there are edges of this type
                edge_traces.append(go.Scatter(
                    x=edge_x, y=edge_y,
                    line=dict(width=1.5, color=edge_colors.get(rel_type, '#888')),
                    hoverinfo='text',
                    text=edge_text,
                    mode='lines',
                    name=rel_type,  # Add legend entry
                    showlegend=True
                ))
        
        # Create node trace with improved visuals
        node_x = []
        node_y = []
        node_text = []
        node_color = []
        node_size = []
        node_symbols = []  # Add different symbols for different entity types
        
        # Define node styling
        color_map = {
            'company': '#1f77b4',    # Blue
            'product': '#ff7f0e',    # Orange
            'market': '#2ca02c',     # Green
            'person': '#d62728'      # Red
        }
        
        symbol_map = {
            'company': 'circle',
            'product': 'diamond',
            'market': 'square',
            'person': 'star'
        }
        
        # Generate node traces grouped by entity type
        entity_types = set()
        for node in subgraph.nodes():
            entity_type = self.graph.nodes[node].get('entity_type', 'unknown')
            entity_types.add(entity_type)
            
        node_traces = []
        for entity_type in entity_types:
            x_coords = []
            y_coords = []
            node_texts = []
            node_sizes = []
            
            for node in subgraph.nodes():
                if self.graph.nodes[node].get('entity_type') == entity_type:
                    x, y = pos[node]
                    x_coords.append(x)
                    y_coords.append(y)
                    
                    # Enhanced hover text
                    attrs = self.graph.nodes[node]
                    connections = subgraph.degree(node)
                    hover_text = f"<b>{node}</b><br>"
                    hover_text += f"Type: {entity_type}<br>"
                    hover_text += f"Connections: {connections}<br>"
                    
                    if entity_type == 'company':
                        if attrs.get('is_user_company'):
                            hover_text += "<br><b>Your Company</b>"
                            node_sizes.append(40)  # Larger size for user company
                        elif attrs.get('is_competitor'):
                            hover_text += "<br><b>Competitor</b>"
                            node_sizes.append(35)  # Large size for competitors
                        else:
                            node_sizes.append(25)
                    else:
                        node_sizes.append(20)
                        
                    node_texts.append(hover_text)
            
            if x_coords:  # Only add trace if there are nodes of this type
                node_traces.append(go.Scatter(
                    x=x_coords, y=y_coords,
                    mode='markers+text',
                    hoverinfo='text',
                    text=[text.split('<br>')[0].replace('<b>', '').replace('</b>', '') for text in node_texts],
                    hovertext=node_texts,
                    textposition="top center",
                    marker=dict(
                        symbol=symbol_map.get(entity_type, 'circle'),
                        color=color_map.get(entity_type, '#7f7f7f'),
                        size=node_sizes,
                        line=dict(width=2, color='white'),
                    ),
                    name=entity_type.capitalize(),
                    showlegend=True
                ))
        
        # Create figure with all traces
        fig = go.Figure(
            data=edge_traces + node_traces,
            layout=go.Layout(
                title=dict(
                    text='Competitive Intelligence Knowledge Graph',
                    font=dict(size=16)
                ),
                showlegend=True,
                hovermode='closest',
                margin=dict(b=20, l=20, r=20, t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                height=800,
                legend=dict(
                    yanchor="top",
                    y=0.99,
                    xanchor="left",
                    x=0.01,
                    bgcolor="rgba(0, 0, 0, 0.8)",
                    bordercolor="rgba(255, 255, 255, 0.2)",
                    borderwidth=1,
                    font=dict(color='white')
                ),
                paper_bgcolor='rgb(17, 17, 17)',
                plot_bgcolor='rgb(17, 17, 17)',
                font=dict(color='white')
            )
        )
        
        # Add better interactivity
        fig.update_layout(
            dragmode='pan',  # Enable panning
            clickmode='event+select'  # Enable node selection
        )
        
        return fig
