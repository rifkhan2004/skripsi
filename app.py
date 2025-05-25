import streamlit as st
import streamlit.components.v1 as components
import json

# Muat data dari data.json
try:
    with open('data.json', 'r') as f:
        data_json_content = json.load(f)
except FileNotFoundError:
    st.error("Kesalahan: data.json tidak ditemukan. Pastikan file berada di direktori yang sama.")
    st.stop()  # Hentikan eksekusi jika file data tidak ditemukan

# Konversi kamus Python ke string JSON untuk disematkan di JavaScript
json_data_str = json.dumps(data_json_content)

# HTML dan JavaScript code to embed in Streamlit
html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Visualisasi Jaringan OII</title>
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
            width: 300px;
            display: none;
        }}
        .connection-list {{
            margin-top: 10px;
            max-height: 200px;
            overflow-y: auto;
            border-top: 1px solid #eee;
            padding-top: 10px;
        }}
        .connection-item {{
            padding: 5px;
            margin: 3px 0;
            background: #f5f5f5;
            border-radius: 3px;
            cursor: pointer;
        }}
        .connection-item:hover {{
            background: #e0e0e0;
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
        </div>
        <div>
            <h3>Cari:</h3>
            <input type="text" id="search-input" placeholder="Cari berdasarkan nama">
        </div>
    </div>
    <div id="node-attributes-panel">
        <h3>Atribut Node: <span id="node-label"></span></h3>
        <div id="node-details"></div>
        <div class="connection-list">
            <h4>Node Terhubung:</h4>
            <div id="connections-container"></div>
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
                minNodeSize: 3,
                maxNodeSize: 15,
                minEdgeSize: 0.5,
                maxEdgeSize: 2,
                enableCamera: true,
                labelThreshold: 5,
                mouseWheelEnabled: true
            }}
        }});

        // Simpan data asli untuk reset
        let originalGraphData = null;

        // Muat data
        s.graph.read(jsonData);
        originalGraphData = JSON.parse(JSON.stringify(jsonData));
        
        // Atur ukuran node berdasarkan degree
        s.graph.nodes().forEach(node => {{
            if (!node.size) {{
                node.size = Math.log(s.graph.degree(node.id) + 1);
            }}
            if (!node.color) {{
                node.color = '#1f77b4';
            }}
            if (!node.label && node.attributes && node.attributes.name) {{
                node.label = node.attributes.name;
            }}
        }});
        
        // Atur warna edge
        s.graph.edges().forEach(edge => {{
            if (!edge.color) {{
                edge.color = '#999';
            }}
        }});
        
        // Refresh tampilan
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
            // Reset semua node ke hidden
            s.graph.nodes().forEach(node => {{
                node.hidden = true;
                node.color = '#1f77b4'; // Reset warna
            }});
            
            // Tampilkan node yang dipilih
            const selectedNode = s.graph.nodes(nodeId);
            if (selectedNode) {{
                selectedNode.hidden = false;
                selectedNode.color = '#d62728'; // Warna merah untuk node yang dipilih
            }}
            
            // Temukan semua node yang terhubung
            const connectedNodes = new Set();
            const connectedEdges = s.graph.edges().filter(edge => {{
                return edge.source === nodeId || edge.target === nodeId;
            }});
            
            connectedEdges.forEach(edge => {{
                const otherNodeId = edge.source === nodeId ? edge.target : edge.source;
                connectedNodes.add(otherNodeId);
                
                // Tampilkan edge yang terhubung
                edge.hidden = false;
                
                // Tampilkan node yang terhubung
                const otherNode = s.graph.nodes(otherNodeId);
                if (otherNode) {{
                    otherNode.hidden = false;
                    otherNode.color = '#ff7f0e'; // Warna oranye untuk node terhubung
                }}
            }});
            
            // Tampilkan node yang dipilih dan edge yang terhubung
            s.refresh();
            
            return Array.from(connectedNodes);
        }}
        
        // Fungsi reset tampilan ke semua node
        function resetView() {{
            s.graph.nodes().forEach(node => {{
                node.hidden = false;
                node.color = '#1f77b4'; // Warna default
            }});
            
            s.graph.edges().forEach(edge => {{
                edge.hidden = false;
            }});
            
            s.refresh();
        }}
        
        // Fungsi tampilkan detail node
        s.bind('clickNode', function(e) {{
            const node = e.data.node;
            const panel = document.getElementById('node-attributes-panel');
            const label = document.getElementById('node-label');
            const details = document.getElementById('node-details');
            const connectionsContainer = document.getElementById('connections-container');
            
            label.textContent = node.label || node.id;
            details.innerHTML = '';
            connectionsContainer.innerHTML = '';
            
            // Tampilkan atribut node
            const attributes = node.attributes || node;
            for (const key in attributes) {{
                if (['x', 'y', 'size', 'color', 'id', 'label'].includes(key)) continue;
                const div = document.createElement('div');
                div.innerHTML = `<strong>${{key}}:</strong> ${{attributes[key]}}`;
                details.appendChild(div);
            }}
            
            // Tampilkan hanya node yang terhubung
            const connectedNodeIds = showConnectedNodes(node.id);
            
            // Tampilkan daftar node yang terhubung
            connectedNodeIds.forEach(nodeId => {{
                const connectedNode = s.graph.nodes(nodeId);
                if (connectedNode) {{
                    const connectionItem = document.createElement('div');
                    connectionItem.className = 'connection-item';
                    connectionItem.textContent = connectedNode.label || connectedNode.id;
                    
                    // Tambahkan event click untuk fokus ke node yang terhubung
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
        }});
        
        // Sembunyikan panel dan reset tampilan saat klik area kosong
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

st.set_page_config(layout="wide")
st.title("Visualisasi Jaringan Interaktif")

st.write("""
Visualisasi jaringan ini menampilkan hubungan antara berbagai entitas. 
Gunakan fitur berikut untuk berinteraksi dengan grafik:
""")

# Render komponen HTML
components.html(html_code, height=850)

jumlah_node = len([node for node in data_json_content.get('nodes', []) 
                  if node.get('id') != '855'])  


st.markdown(f"""
### Panduan Penggunaan:
1. **Klik Node**: Klik pada node (misalnya "TimnasIndonesia") untuk melihat:
   - Detail atribut node
   - Daftar node yang terhubung
   - Hanya node yang terhubung yang akan ditampilkan di grafik
2. **Klik Nama di Daftar**: Klik nama node di daftar koneksi untuk fokus ke node tersebut
3. **Klik Area Kosong**: Kembalikan tampilan ke semua node
4. **Drag Node**: Klik dan tahan node untuk memindahkannya
5. **Zoom**: Gunakan scroll mouse untuk zoom in/out

### Informasi Teknis:
- **Jumlah Node**: {jumlah_node}
- **Jumlah Edge**: {len(data_json_content.get('edges', []))}
""")
