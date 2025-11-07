# Knowledge Graph Feature Guide

## Overview

The CEO AI Assistant now includes a powerful **Knowledge Graph** feature that enables sophisticated competitive intelligence analysis by tracking relationships between companies, competitors, products, markets, and people.

## What is a Knowledge Graph?

A knowledge graph is a network of interconnected entities and their relationships. Instead of just storing information about individual companies, it captures:

- **Entities**: Companies, products, markets, people
- **Relationships**: Who competes with whom, which company produces which products, who works where, etc.
- **Attributes**: Revenue, market position, roles, categories, etc.

This allows the AI to answer complex, multi-hop queries that simple analysis cannot handle.

## Key Features

### 1. **Automatic Graph Building**
- When you identify competitors, they are automatically added to the knowledge graph
- Competitive relationships are established between your company and identified competitors
- As you analyze competitors, entities are extracted and added to the graph

### 2. **Entity Types Tracked**
- **Companies**: Your company and all competitors
- **Products**: Products and services offered by companies
- **Markets**: Industry segments and market spaces
- **People**: Executives, founders, and key personnel

### 3. **Relationship Types**
- `competes_with`: Competitive relationships
- `produces`: Company produces a product
- `operates_in`: Company operates in a market
- `works_at`: Person works at a company
- `partners_with`: Partnership relationships

### 4. **Intelligent Query Routing**

The system automatically detects when to use the knowledge graph:

**Keywords that trigger Knowledge Graph Analysis:**
- "compare"
- "relationship"
- "connection"
- "shared"
- "common"
- "network"
- "indirect"
- "all competitors"
- "markets"
- "overlap"

**Example Queries:**
- ✅ "What markets do we share with our competitors?"
- ✅ "Show me the relationship between [Company A] and [Company B]"
- ✅ "What products overlap between us and [Competitor]?"
- ✅ "Compare all our competitors' market positions"
- ✅ "What indirect connections exist between [Company A] and [Company B]?"

**Simple queries use regular analysis:**
- "What is [Competitor]'s revenue?"
- "Tell me about [Company]'s latest product"
- "What are the risks from [Competitor]?"

## Visualization

The knowledge graph can be visualized in the **Detailed Analysis** tab:

**Node Colors:**
- 🔵 Blue: Companies
- 🟠 Orange: Products
- 🟢 Green: Markets
- 🔴 Red: People

**Node Sizes:**
- Larger nodes = more connections
- Smaller nodes = fewer connections

**Interactive Features:**
- Hover over nodes to see details
- Hover over edges to see relationship types
- Pan and zoom to explore

## Advanced Capabilities

### 1. **Multi-Hop Queries**
The graph can trace indirect relationships:
- "Is there a connection between [Company A] and [Company C] through [Company B]?"
- "What shared suppliers do our competitors have?"

### 2. **Market Overlap Analysis**
Identify where competitors are competing in the same spaces:
- "Which competitors operate in the cloud computing market?"
- "Show all companies in the electric vehicle market"

### 3. **Network Analysis**
Understand the broader competitive ecosystem:
- "Who are the most connected players in our industry?"
- "What is our position in the competitive network?"

### 4. **Strategic Insights**
The graph helps identify:
- Hidden competitive threats
- Partnership opportunities
- Market gaps
- Ecosystem dynamics

## Example Usage Workflow

1. **Start Analysis**: Enter your company name
2. **Identify Competitors**: AI identifies top 3 competitors → Graph is initialized
3. **Analyze Competitor**: Select a competitor → AI extracts entities → Graph expands
4. **View Graph**: Check "Knowledge Graph Visualization" in Detailed Analysis tab
5. **Ask Complex Questions**: Use graph-aware queries in chat

## Technical Details

### Graph Structure
- **Directed Multi-Graph**: Allows multiple relationships between entities
- **Attributes on Nodes**: Store entity properties (revenue, market cap, etc.)
- **Attributes on Edges**: Store relationship metadata (date established, strength, etc.)

### Query Methods Available

The `CompetitiveKnowledgeGraph` class provides:

```python
# Company queries
get_competitors(company)
get_company_products(company)
get_company_leadership(company)
get_company_network(company, depth)

# Market queries
get_shared_markets(company1, company2)
get_market_landscape(market)

# Relationship queries
get_relationship_path(source, target, max_length)
find_competitive_threats(user_company, competitor)

# Entity queries
query_entities_by_attribute(entity_type, attribute, value)

# Analysis
get_graph_summary()
export_graph_data()
```

## Benefits

### 1. **More Nuanced Analysis**
- Understands context and relationships
- Provides insights that simple searches miss
- Identifies non-obvious connections

### 2. **Complex Query Handling**
- Multi-entity comparisons
- Cross-market analysis
- Ecosystem-wide insights

### 3. **Strategic Decision Making**
- Visualize competitive landscape
- Identify partnership opportunities
- Spot market gaps

### 4. **Cumulative Intelligence**
- Knowledge accumulates over time
- Historical relationships tracked
- Persistent competitive insights

## Future Enhancements (Roadmap)

- [ ] Export graph to Neo4j or other graph databases
- [ ] Temporal analysis (track changes over time)
- [ ] Sentiment analysis on relationships
- [ ] Automatic entity extraction from documents
- [ ] Graph-based recommendations
- [ ] Community detection (identify market clusters)
- [ ] Centrality analysis (find key players)

## Tips for Best Results

1. **Be Specific in Queries**: The more specific your question, the better the graph can help
2. **Use Comparison Keywords**: Trigger graph analysis with words like "compare", "shared", "overlap"
3. **Analyze Multiple Competitors**: The more competitors you analyze, the richer the graph becomes
4. **Check Visualization**: The visual graph helps identify patterns you might miss in text
5. **Ask Follow-up Questions**: Use the context from previous analyses to ask deeper questions

## Troubleshooting

**Graph seems empty?**
- Ensure you've analyzed at least one competitor
- Check that competitor analysis completed successfully

**Visualization not showing?**
- Verify that networkx and plotly are installed
- Check browser console for errors
- Try refreshing the page

**Queries not using knowledge graph?**
- Use specific keywords like "compare", "shared", "relationship"
- Try rephrasing your question to be more comparative

## Support

For issues or questions:
1. Check console logs for errors
2. Verify all dependencies are installed: `pip install -r requirements.txt`
3. Ensure API keys are properly configured

---

**Note**: The knowledge graph is stored in session state. Starting a new session will create a fresh graph. Future versions will support graph persistence.
