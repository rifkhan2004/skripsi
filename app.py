import streamlit as st
import streamlit.components.v1 as components
import json

# Load data from data.json
try:
    with open('data.json', 'r') as f:
        data_json_content = json.load(f)
except FileNotFoundError:
    st.error("Error: data.json not found. Please ensure the file is in the same directory.")
    st.stop()

# Convert Python dict to JSON string for JavaScript embedding
json_data_str = json.dumps(data_json_content)

# HTML and JavaScript code to embed in Streamlit
html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Network Visualization</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {{ margin: 0; overflow: hidden; font-family: sans-serif; }}
        #sigma-container {{ 
            width: 100%;
            height: 800px;
            border: 1px solid #ccc;
            background-color: #f0f0f0;
        }}
        #mainpanel {{
            position: absolute;
            top: 20px;
            left: 20px;
            background: rgba(255, 255, 255, 0.9);
            padding: 15px;
            border-radius: 8px;
            z-index: 100;
            max-height: 80%;
            overflow-y: auto;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            width: 280px;
        }}
        #node-attributes-panel {{
            position: absolute;
            top: 20px;
            right: 20px;
            background: rgba(255, 255, 255, 0.95);
            padding: 15px;
            border-radius: 8px;
            z-index: 90;
            max-height: 80%;
            overflow-y: auto;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            width: 350px;
            display: none;
        }}
        .connection-list {{
            margin-top: 10px;
            max-height: 300px;
            overflow-y: auto;
            border-top: 1px solid #eee;
            padding-top: 10px;
        }}
        .connection-item {{
            padding: 10px;
            margin: 5px 0;
            background: #f5f5f5;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.2s;
            position: relative;
            padding-left: 25px;
        }}
        .connection-item:hover {{
            background: #e0e0e0;
        }}
        .connection-indicator {{
            position: absolute;
            left: 8px;
            top: 13px;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            border: 1px solid;
        }}
        .out-connection .connection-indicator {{
            background-color: #d62728;
            border-color: #a11c1c;
        }}
        .in-connection .connection-indicator {{
            background-color: #2ca02c;
            border-color: #1c6e1c;
        }}
        .both-connection .connection-indicator {{
            background: linear-gradient(135deg, #d62728 50%, #2ca02c 50%);
            border-color: #7a1c1c;
        }}
        .connection-header {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 5px;
        }}
        .connection-name {{
            font-weight: bold;
        }}
        .connection-stats {{
            display: flex;
            justify-content: space-between;
            font-size: 0.9em;
            color: #555;
        }}
        .stat-item {{
            margin-right: 10px;
        }}
        .out-degree {{ color: #d62728; }}
        .in-degree {{ color: #2ca02c; }}
        .total-degree {{ color: #1f77b4; }}
        .attribute-item {{
            margin-bottom: 8px;
            padding-bottom: 8px;
            border-bottom: 1px solid #eee;
        }}
        .attribute-key {{
            font-weight: bold;
            color: #333;
        }}
        .attribute-value {{
            color: #555;
        }}
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/sigma.js/1.2.1/sigma.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/sigma.js/1.2.1/plugins/sigma.parsers.json.min.js"></script>
</head>
<body>
    <div id="sigma-container"></div>
    <div id="mainpanel">
        <h2>Network Visualization</h2>
        <p>This is a sample network visualization.</p>
        <div>
            <h3>Legend:</h3>
            <p><strong style="color: #1f77b4;">Node</strong>: Represents an entity</p>
            <p><strong style="color: #999;">Edge</strong>: Represents a connection</p>
            <p><strong style="color: #ff7f0e;">Connected Node</strong>: Nodes connected to selected node</p>
            <p><strong style="color: #d62728;">Selected Node</strong>: Currently selected node</p>
        </div>
        <div>
            <h3>Search:</h3>
            <input type="text" id="search-input" placeholder="Search by name">
        </div>
    </div>
    <div id="node-attributes-panel">
        <h3>Node Attributes: <span id="node-label"></span></h3>
        <div id="node-details"></div>
        <div class="connection-list">
            <h4>Connected Nodes (<span id="connection-count">0</span>):</h4>
            <div id="connections-container"></div>
        </div>
    </div>

    <script>
        // Network data
        const jsonData = {json_data_str};
        
        // Initialize sigma
        const container = document.getElementById('sigma-container');
        const s = new sigma({{
            container: container,
            settings: {{
                minNodeSize: 5,
                maxNodeSize: 20,
                minEdgeSize: 1,
                maxEdgeSize: 3,
                enableCamera: true,
                labelThreshold: 8,
                mouseWheelEnabled: true
            }}
        }});

        // Load data
        s.graph.read(jsonData);
        
        // Calculate degrees for all nodes
        function calculateDegrees() {{
            s.graph.nodes().forEach(node => {{
                node.outDegree = s.graph.outEdges(node.id).length;
                node.inDegree = s.graph.inEdges(node.id).length;
                node.degree = node.outDegree + node.inDegree;
                
                if (!node.size) {{
                    node.size = Math.log(node.degree + 1) * 2;
                }}
                if (!node.color) {{
                    node.color = '#1f77b4';
                }}
                if (!node.label && node.attributes && node.attributes.name) {{
                    node.label = node.attributes.name;
                }}
            }});
        }}
        
        calculateDegrees();
        
        // Set edge colors
        s.graph.edges().forEach(edge => {{
            if (!edge.color) {{
                edge.color = '#999';
            }}
        }});
        
        s.refresh();
        
        // Search functionality
        document.getElementById('search-input').addEventListener('input', function(e) {{
            const query = e.target.value.toLowerCase();
            s.graph.nodes().forEach(node => {{
                const label = (node.label || node.id || '').toLowerCase();
                node.hidden = query !== '' && !label.includes(query);
            }});
            s.refresh();
        }});
        
        // Function to determine connection type
        function getConnectionType(sourceId, targetId) {{
            const outEdges = s.graph.edges().filter(e => e.source === sourceId && e.target === targetId);
            const inEdges = s.graph.edges().filter(e => e.source === targetId && e.target === sourceId);
            
            if (outEdges.length > 0 && inEdges.length > 0) {{
                return {{ 
                    type: 'both', 
                    class: 'both-connection',
                    label: 'Bidirectional',
                    symbol: '↔'
                }};
            }} else if (outEdges.length > 0) {{
                return {{ 
                    type: 'out', 
                    class: 'out-connection',
                    label: 'Outgoing',
                    symbol: '→'
                }};
            }} else if (inEdges.length > 0) {{
                return {{ 
                    type: 'in', 
                    class: 'in-connection',
                    label: 'Incoming',
                    symbol: '←'
                }};
            }}
            return {{ 
                type: 'none', 
                class: '',
                label: '',
                symbol: ''
            }};
        }}

        // Show node details
        s.bind('clickNode', function(e) {{
            const node = e.data.node;
            const panel = document.getElementById('node-attributes-panel');
            const label = document.getElementById('node-label');
            const details = document.getElementById('node-details');
            const connectionsContainer = document.getElementById('connections-container');
            const connectionCount = document.getElementById('connection-count');
            
            label.textContent = node.label || node.id;
            details.innerHTML = '';
            connectionsContainer.innerHTML = '';
            
            // Show node attributes
            const attributes = node.attributes || node;
            for (const key in attributes) {{
                if (['x', 'y', 'size', 'color', 'id', 'label'].includes(key)) continue;
                
                const div = document.createElement('div');
                div.className = 'attribute-item';
                
                const keySpan = document.createElement('span');
                keySpan.className = 'attribute-key';
                keySpan.textContent = key + ': ';
                
                const valueSpan = document.createElement('span');
                valueSpan.className = 'attribute-value';
                valueSpan.textContent = attributes[key];
                
                div.appendChild(keySpan);
                div.appendChild(valueSpan);
                details.appendChild(div);
            }}
            
            // Show connected nodes
            const connectedNodeIds = new Set();
            const connectedEdges = s.graph.edges().filter(edge => {{
                return edge.source === node.id || edge.target === node.id;
            }});
            
            connectedEdges.forEach(edge => {{
                const otherNodeId = edge.source === node.id ? edge.target : edge.source;
                connectedNodeIds.add(otherNodeId);
            }});
            
            connectionCount.textContent = connectedNodeIds.size;
            
            // Display connected nodes with connection type indicators
            connectedNodeIds.forEach(nodeId => {{
                const connectedNode = s.graph.nodes(nodeId);
                if (connectedNode) {{
                    const connectionType = getConnectionType(node.id, connectedNode.id);
                    const connectionItem = document.createElement('div');
                    connectionItem.className = `connection-item ${{connectionType.class}}`;
                    
                    // Connection indicator
                    const indicator = document.createElement('div');
                    indicator.className = 'connection-indicator';
                    indicator.title = connectionType.label;
                    
                    // Connection header
                    const header = document.createElement('div');
                    header.className = 'connection-header';
                    
                    const nameSpan = document.createElement('span');
                    nameSpan.className = 'connection-name';
                    nameSpan.textContent = connectedNode.label || connectedNode.id;
                    
                    const directionSpan = document.createElement('span');
                    directionSpan.textContent = connectionType.symbol;
                    directionSpan.style.marginLeft = '5px';
                    
                    header.appendChild(nameSpan);
                    header.appendChild(directionSpan);
                    
                    // Connection stats
                    const stats = document.createElement('div');
                    stats.className = 'connection-stats';
                    
                    stats.innerHTML = `
                        <span class="stat-item"><span class="out-degree">Out: ${{connectedNode.outDegree || 0}}</span></span>
                        <span class="stat-item"><span class="in-degree">In: ${{connectedNode.inDegree || 0}}</span></span>
                        <span class="stat-item"><span class="total-degree">Total: ${{connectedNode.degree || 0}}</span></span>
                    `;
                    
                    // Combine all elements
                    connectionItem.appendChild(indicator);
                    connectionItem.appendChild(header);
                    connectionItem.appendChild(stats);
                    
                    // Click to focus on connected node
                    connectionItem.addEventListener('click', () => {{
                        s.camera.goTo({{
                            x: connectedNode.x,
                            y: connectedNode.y,
                            ratio: 0.8
                        }});
                    }});
                    
                    connectionsContainer.appendChild(connectionItem);
                }}
            }});
            
            panel.style.display = 'block';
            
            // Highlight connected nodes in the visualization
            s.graph.nodes().forEach(n => {{
                n.hidden = true;
                n.color = '#1f77b4';
            }});
            
            // Show selected node
            node.hidden = false;
            node.color = '#d62728';
            
            // Show connected nodes
            connectedNodeIds.forEach(nodeId => {{
                const connectedNode = s.graph.nodes(nodeId);
                if (connectedNode) {{
                    connectedNode.hidden = false;
                    connectedNode.color = '#ff7f0e';
                }}
            }});
            
            s.refresh();
        }});
        
        // Reset view when clicking on empty space
        s.bind('clickStage', function() {{
            document.getElementById('node-attributes-panel').style.display = 'none';
            
            // Reset all nodes to visible
            s.graph.nodes().forEach(node => {{
                node.hidden = false;
                node.color = '#1f77b4';
            }});
            
            s.refresh();
        }});
        
        // Enable node dragging
        s.bind('downNode', function(e) {{
            const node = e.data.node;
            node.isDragging = true;
        }});
        
        s.bind('mouseup', function() {{
            s.graph.nodes().forEach(node => {{
                node.isDragging = false;
            }});
        }});
        
        s.bind('mousemove', function(e) {{
            const draggedNode = s.graph.nodes().find(node => node.isDragging);
            if (draggedNode) {{
                draggedNode.x = e.data.captor.x;
                draggedNode.y = e.data.captor.y;
                s.refresh();
            }}
        }});
    </script>
</body>
</html>
"""

# Streamlit app configuration
st.set_page_config(layout="wide")
st.title("Interactive Network Visualization")

st.write("""
This network visualization displays relationships between various entities.
Use the following features to interact with the graph:
""")

# Render the HTML component
components.html(html_code, height=850)

st.markdown(f"""
### User Guide:
1. **Click Node**: Click on a node (e.g., "TimnasIndonesia") to see:
   - Node attributes including network metrics
   - List of connected nodes with out-degree and in-degree information
   - Only connected nodes will be displayed in the graph
2. **Click Name in List**: Click a node name in the connections list to focus on that node
3. **Click Empty Area**: Reset the view to show all nodes
4. **Drag Node**: Click and hold a node to move it
5. **Zoom**: Use mouse wheel to zoom in/out

### Technical Information:
- **Node Count**: {len(data_json_content.get('nodes', []))}
- **Edge Count**: {len(data_json_content.get('edges', []))}
""")
