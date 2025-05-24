import streamlit as st
import streamlit.components.v1 as components
import json

# Muat data dari data.json
try:
    with open('data.json', 'r') as f:
        data_json_content = json.load(f)
except FileNotFoundError:
    st.error("Kesalahan: data.json tidak ditemukan. Pastikan file berada di direktori yang sama.")
    st.stop()

# Konversi kamus Python ke string JSON untuk disematkan di JavaScript
json_data_str = json.dumps(data_json_content)

html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Visualisasi Jaringan</title>
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
        .connection-section {{
            margin-top: 15px;
        }}
        .connection-section h4 {{
            margin-bottom: 8px;
            padding-bottom: 5px;
            border-bottom: 2px solid #eee;
        }}
        .connection-list {{
            max-height: 200px;
            overflow-y: auto;
            margin-bottom: 15px;
        }}
        .connection-item {{
            padding: 10px;
            margin: 5px 0;
            background: #f5f5f5;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.2s;
        }}
        .connection-item:hover {{
            background: #e0e0e0;
        }}
        .connection-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 5px;
        }}
        .connection-name {{
            font-weight: bold;
            font-size: 1.1em;
        }}
        .connection-direction {{
            font-size: 1.2em;
            margin: 0 5px;
        }}
        .connection-stats {{
            display: flex;
            justify-content: space-between;
            font-size: 0.9em;
            color: #555;
            margin-top: 5px;
        }}
        .stat-item {{
            display: flex;
            align-items: center;
        }}
        .stat-label {{
            margin-right: 5px;
            font-weight: bold;
        }}
        .in-degree-section h4 {{ color: #2ca02c; }}
        .out-degree-section h4 {{ color: #d62728; }}
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
        .connection-count {{
            font-weight: normal;
            font-size: 0.9em;
            color: #666;
        }}
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/sigma.js/1.2.1/sigma.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/sigma.js/1.2.1/plugins/sigma.parsers.json.min.js"></script>
</head>
<body>
    <div id="sigma-container"></div>
    <div id="mainpanel">
        <h2>Visualisasi Jaringan</h2>
        <p>Ini adalah contoh visualisasi jaringan.</p>
        <div>
            <h3>Legenda:</h3>
            <p><strong style="color: #1f77b4;">Node</strong>: Mewakili entitas</p>
            <p><strong style="color: #999;">Edge</strong>: Mewakili koneksi</p>
            <p><strong style="color: #ff7f0e;">Node Terhubung</strong>: Node yang berhubungan dengan node yang dipilih</p>
            <p><strong style="color: #d62728;">Node Dipilih</strong>: Node yang sedang dipilih</p>
        </div>
        <div>
            <h3>Cari:</h3>
            <input type="text" id="search-input" placeholder="Cari berdasarkan nama">
        </div>
    </div>
    <div id="node-attributes-panel">
        <h3>Atribut Node: <span id="node-label"></span></h3>
        <div id="node-details"></div>
        
        <div class="connection-section out-degree-section">
            <h4>Out-Degree Connections <span class="connection-count" id="out-degree-count">(0)</span></h4>
            <div class="connection-list" id="out-degree-connections"></div>
        </div>
        
        <div class="connection-section in-degree-section">
            <h4>In-Degree Connections <span class="connection-count" id="in-degree-count">(0)</span></h4>
            <div class="connection-list" id="in-degree-connections"></div>
        </div>
    </div>

    <script>
        // Data jaringan
        const jsonData = {json_data_str};
        
        // Inisialisasi sigma
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

        // Muat data
        s.graph.read(jsonData);
        
        // Hitung degree untuk semua node
        function calculateDegrees() {{
            s.graph.nodes().forEach(node => {{
                node.outDegree = s.graph.outEdges(node.id).length;
                node.inDegree = s.graph.inEdges(node.id).length;
                node.degree = node.outDegree + node.inDegree;
                
                if (!node.size) node.size = Math.log(node.degree + 1) * 2;
                if (!node.color) node.color = '#1f77b4';
                if (!node.label && node.attributes && node.attributes.name) node.label = node.attributes.name;
            }});
        }}
        
        calculateDegrees();
        
        // Atur warna edge
        s.graph.edges().forEach(edge => {{
            if (!edge.color) edge.color = '#999';
        }});
        
        s.refresh();
        
        // Fungsi pencarian
        document.getElementById('search-input').addEventListener('input', function(e) {{
            const query = e.target.value.toLowerCase();
            s.graph.nodes().forEach(node => {{
                const label = (node.label || node.id || '').toLowerCase();
                node.hidden = query !== '' && !label.includes(query);
            }});
            s.refresh();
        }});
        
        // Fungsi untuk menampilkan hanya node yang terhubung
        function showConnectedNodes(nodeId) {{
            s.graph.nodes().forEach(node => {{
                node.hidden = true;
                node.color = '#1f77b4';
            }});
            
            const selectedNode = s.graph.nodes(nodeId);
            if (selectedNode) {{
                selectedNode.hidden = false;
                selectedNode.color = '#d62728';
            }}
            
            const connectedNodes = new Set();
            const connectedEdges = s.graph.edges().filter(edge => {{
                return edge.source === nodeId || edge.target === nodeId;
            }});
            
            connectedEdges.forEach(edge => {{
                const otherNodeId = edge.source === nodeId ? edge.target : edge.source;
                connectedNodes.add(otherNodeId);
                edge.hidden = false;
                
                const otherNode = s.graph.nodes(otherNodeId);
                if (otherNode) {{
                    otherNode.hidden = false;
                    otherNode.color = '#ff7f0e';
                }}
            }});
            
            s.refresh();
            return Array.from(connectedNodes);
        }}
        
        // Fungsi reset tampilan
        function resetView() {{
            s.graph.nodes().forEach(node => {{
                node.hidden = false;
                node.color = '#1f77b4';
            }});
            s.graph.edges().forEach(edge => edge.hidden = false);
            s.refresh();
        }}
        
        // Fungsi tampilkan detail node
        s.bind('clickNode', function(e) {{
            const node = e.data.node;
            const panel = document.getElementById('node-attributes-panel');
            const label = document.getElementById('node-label');
            const details = document.getElementById('node-details');
            const outDegreeConnections = document.getElementById('out-degree-connections');
            const inDegreeConnections = document.getElementById('in-degree-connections');
            const outDegreeCount = document.getElementById('out-degree-count');
            const inDegreeCount = document.getElementById('in-degree-count');
            
            label.textContent = node.label || node.id;
            details.innerHTML = '';
            outDegreeConnections.innerHTML = '';
            inDegreeConnections.innerHTML = '';
            
            // Tampilkan atribut node
            const attributes = node.attributes || node;
            for (const key in attributes) {{
                if (['x', 'y', 'size', 'color', 'id', 'label'].includes(key)) continue;
                
                const div = document.createElement('div');
                div.className = 'attribute-item';
                div.innerHTML = `
                    <span class="attribute-key">${{key}}:</span>
                    <span class="attribute-value">${{attributes[key]}}</span>
                `;
                details.appendChild(div);
            }}
            
            // Tampilkan hanya node yang terhubung
            const connectedNodeIds = showConnectedNodes(node.id);
            
            // Pisahkan koneksi berdasarkan arah
            let outDegreeNodes = [];
            let inDegreeNodes = [];
            
            connectedNodeIds.forEach(nodeId => {{
                const connectedNode = s.graph.nodes(nodeId);
                if (connectedNode) {{
                    const edgesFromSelected = s.graph.edges().filter(e => e.source === node.id && e.target === connectedNode.id);
                    const edgesToSelected = s.graph.edges().filter(e => e.source === connectedNode.id && e.target === node.id);
                    
                    if (edgesFromSelected.length > 0) {{
                        outDegreeNodes.push(connectedNode);
                    }}
                    if (edgesToSelected.length > 0) {{
                        inDegreeNodes.push(connectedNode);
                    }}
                }}
            }});
            
            // Update count
            outDegreeCount.textContent = `(${{outDegreeNodes.length}})`;
            inDegreeCount.textContent = `(${{inDegreeNodes.length}})`;
            
            // Tampilkan out-degree connections
            outDegreeNodes.forEach(connectedNode => {{
                const connectionItem = createConnectionItem(node, connectedNode, '→');
                outDegreeConnections.appendChild(connectionItem);
            }});
            
            // Tampilkan in-degree connections
            inDegreeNodes.forEach(connectedNode => {{
                const connectionItem = createConnectionItem(node, connectedNode, '←');
                inDegreeConnections.appendChild(connectionItem);
            }});
            
            panel.style.display = 'block';
        }});
        
        // Fungsi untuk membuat item koneksi
        function createConnectionItem(mainNode, connectedNode, directionSymbol) {{
            const connectionItem = document.createElement('div');
            connectionItem.className = 'connection-item';
            
            // Header
            const header = document.createElement('div');
            header.className = 'connection-header';
            header.innerHTML = `
                <span class="connection-name">${{connectedNode.label || connectedNode.id}}</span>
                <span class="connection-direction">${{directionSymbol}}</span>
            `;
            
            // Stats
            const stats = document.createElement('div');
            stats.className = 'connection-stats';
            stats.innerHTML = `
                <div class="stat-item">
                    <span class="stat-label">Out:</span>
                    <span class="out-degree">${{connectedNode.outDegree || 0}}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">In:</span>
                    <span class="in-degree">${{connectedNode.inDegree || 0}}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Total:</span>
                    <span class="total-degree">${{connectedNode.degree || 0}}</span>
                </div>
            `;
            
            connectionItem.appendChild(header);
            connectionItem.appendChild(stats);
            
            // Click event
            connectionItem.addEventListener('click', () => {{
                s.camera.goTo({{
                    x: connectedNode.x,
                    y: connectedNode.y,
                    ratio: 0.8
                }});
            }});
            
            return connectionItem;
        }}
        
        // Sembunyikan panel saat klik area kosong
        s.bind('clickStage', function() {{
            document.getElementById('node-attributes-panel').style.display = 'none';
            resetView();
        }});
        
        // Enable drag nodes
        s.bind('downNode', function(e) {{
            const node = e.data.node;
            node.isDragging = true;
        }});
        
        s.bind('mouseup', function() {{
            s.graph.nodes().forEach(node => node.isDragging = false);
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

st.set_page_config(layout="wide")
st.title("Visualisasi Jaringan Interaktif")

st.write("""
Visualisasi jaringan ini menampilkan hubungan antara berbagai entitas. 
Gunakan fitur berikut untuk berinteraksi dengan grafik:
""")

# Render komponen HTML
components.html(html_code, height=850)

st.markdown(f"""
### Panduan Penggunaan:
1. **Klik Node**: Klik pada node (misalnya "TimnasIndonesia") untuk melihat:
   - Detail atribut node
   - Daftar node terhubung yang dibagi menjadi:
     - **Out-Degree**: Node yang menerima koneksi dari node ini
     - **In-Degree**: Node yang mengirim koneksi ke node ini
2. **Klik Nama di Daftar**: Klik nama node di daftar koneksi untuk fokus ke node tersebut
3. **Klik Area Kosong**: Kembalikan tampilan ke semua node
4. **Drag Node**: Klik dan tahan node untuk memindahkannya
5. **Zoom**: Gunakan scroll mouse untuk zoom in/out

### Informasi Teknis:
- **Jumlah Node**: {len(data_json_content.get('nodes', []))}
- **Jumlah Edge**: {len(data_json_content.get('edges', []))}
""")
