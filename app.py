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
        .connection-header {{
            margin-bottom: 5px;
            padding-bottom: 5px;
            font-weight: bold;
        }}
        .incoming-header {{
            color: #2ca02c;
        }}
        .outgoing-header {{
            color: #ff7f0e;
        }}
        .connection-names {{
            display: flex;
            flex-wrap: wrap;
            gap: 5px;
        }}
        .name-item {{
            padding: 2px 5px;
            border-radius: 3px;
            cursor: pointer;
        }}
        .incoming-name {{
            color: #2ca02c;
        }}
        .outgoing-name {{
            color: #ff7f0e;
        }}
        .name-item:hover {{
            text-decoration: underline;
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
            <p><strong style="color: #2ca02c;">Incoming</strong>: Node yang mengarah ke node yang dipilih</p>
            <p><strong style="color: #ff7f0e;">Outgoing</strong>: Node yang dituju dari node yang dipilih</p>
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
        
        // Fungsi untuk mendapatkan node yang terhubung (incoming dan outgoing)
        function getConnectedNodes(nodeId) {{
            const connectedNodes = {{
                incoming: [],
                outgoing: []
            }};
            
            s.graph.edges().forEach(edge => {{
                if (edge.source === nodeId) {{
                    connectedNodes.outgoing.push(edge.target);
                }} else if (edge.target === nodeId) {{
                    connectedNodes.incoming.push(edge.source);
                }}
            }});
            
            return connectedNodes;
        }}
        
        // Fungsi untuk menampilkan hanya node yang terhubung
        function showConnectedNodes(nodeId) {{
            // Reset semua node ke hidden
            s.graph.nodes().forEach(node => {{
                node.hidden = true;
                node.color = '#1f77b4';
            }});
            
            // Tampilkan node yang dipilih
            const selectedNode = s.graph.nodes(nodeId);
            if (selectedNode) {{
                selectedNode.hidden = false;
                selectedNode.color = '#d62728';
            }}
            
            // Dapatkan node yang terhubung
            const connectedNodes = getConnectedNodes(nodeId);
            const allConnectedNodes = [...connectedNodes.incoming, ...connectedNodes.outgoing];
            
            // Tampilkan node yang terhubung dengan warna berbeda
            connectedNodes.incoming.forEach(otherNodeId => {{
                const otherNode = s.graph.nodes(otherNodeId);
                if (otherNode) {{
                    otherNode.hidden = false;
                    otherNode.color = '#2ca02c'; // Hijau untuk incoming
                }}
            }});
            
            connectedNodes.outgoing.forEach(otherNodeId => {{
                const otherNode = s.graph.nodes(otherNodeId);
                if (otherNode) {{
                    otherNode.hidden = false;
                    otherNode.color = '#ff7f0e'; // Oranye untuk outgoing
                }}
            }});
            
            // Tampilkan edge yang terhubung
            s.graph.edges().forEach(edge => {{
                edge.hidden = !(allConnectedNodes.includes(edge.source) || allConnectedNodes.includes(edge.target));
            }});
            
            s.refresh();
            
            return connectedNodes;
        }}
        
        // Fungsi reset tampilan ke semua node
        function resetView() {{
            s.graph.nodes().forEach(node => {{
                node.hidden = false;
                node.color = '#1f77b4';
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
            
            // Tampilkan hanya node yang terhubung dan dapatkan daftar terpisah
            const connectedNodes = showConnectedNodes(node.id);
            
            // Tampilkan daftar incoming connections
            if (connectedNodes.incoming.length > 0) {{
                const incomingHeader = document.createElement('div');
                incomingHeader.className = 'connection-header incoming-header';
                incomingHeader.textContent = `Incoming (${{connectedNodes.incoming.length}})`;
                connectionsContainer.appendChild(incomingHeader);
                
                const incomingNamesContainer = document.createElement('div');
                incomingNamesContainer.className = 'connection-names';
                
                connectedNodes.incoming.forEach(nodeId => {{
                    const connectedNode = s.graph.nodes(nodeId);
                    if (connectedNode) {{
                        const nameItem = document.createElement('span');
                        nameItem.className = 'name-item incoming-name';
                        nameItem.textContent = connectedNode.label || connectedNode.id;
                        
                        nameItem.addEventListener('click', () => {{
                            s.camera.goTo({{
                                x: connectedNode.x,
                                y: connectedNode.y,
                                ratio: 0.8
                            }});
                        }});
                        
                        incomingNamesContainer.appendChild(nameItem);
                    }}
                }});
                
                connectionsContainer.appendChild(incomingNamesContainer);
            }}
            
            // Tampilkan daftar outgoing connections
            if (connectedNodes.outgoing.length > 0) {{
                const outgoingHeader = document.createElement('div');
                outgoingHeader.className = 'connection-header outgoing-header';
                outgoingHeader.textContent = `Outgoing (${{connectedNodes.outgoing.length}})`;
                connectionsContainer.appendChild(outgoingHeader);
                
                const outgoingNamesContainer = document.createElement('div');
                outgoingNamesContainer.className = 'connection-names';
                
                connectedNodes.outgoing.forEach(nodeId => {{
                    const connectedNode = s.graph.nodes(nodeId);
                    if (connectedNode) {{
                        const nameItem = document.createElement('span');
                        nameItem.className = 'name-item outgoing-name';
                        nameItem.textContent = connectedNode.label || connectedNode.id;
                        
                        nameItem.addEventListener('click', () => {{
                            s.camera.goTo({{
                                x: connectedNode.x,
                                y: connectedNode.y,
                                ratio: 0.8
                            }});
                        }});
                        
                        outgoingNamesContainer.appendChild(nameItem);
                    }}
                }});
                
                connectionsContainer.appendChild(outgoingNamesContainer);
            }}
            
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

st.markdown(f"""
### Panduan Penggunaan:
1. **Klik Node**: Klik pada node untuk melihat:
   - Detail atribut node
   - Daftar node yang terhubung (dibedakan antara incoming dan outgoing)
   - Hanya node yang terhubung yang akan ditampilkan di grafik
2. **Klik Nama di Daftar**: Klik nama node di daftar koneksi untuk fokus ke node tersebut
3. **Klik Area Kosong**: Kembalikan tampilan ke semua node
4. **Drag Node**: Klik dan tahan node untuk memindahkannya
5. **Zoom**: Gunakan scroll mouse untuk zoom in/out

### Legenda Warna:
- **Merah**: Node yang sedang dipilih
- **Hijau**: Node incoming (mengarah ke node yang dipilih)
- **Oranye**: Node outgoing (dituju dari node yang dipilih)
- **Biru**: Node biasa

### Informasi Teknis:
- **Jumlah Node**: {len(data_json_content.get('nodes', []))}
- **Jumlah Edge**: {len(data_json_content.get('edges', []))}
""")
