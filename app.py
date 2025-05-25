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
        .connection-section {{
            margin-bottom: 15px;
        }}
        .connection-header {{
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .mutual-header {{ color: #9467bd; }}
        .incoming-header {{ color: #2ca02c; }}
        .outgoing-header {{ color: #ff7f0e; }}
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
        .mutual-name {{ color: #9467bd; }}
        .incoming-name {{ color: #2ca02c; }}
        .outgoing-name {{ color: #ff7f0e; }}
        .name-item:hover {{
            text-decoration: underline;
            background-color: #f0f0f0;
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
            <p><strong style="color: #9467bd;">Mutual</strong>: Koneksi dua arah</p>
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
            <h4>Connections:</h4>
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

        // Muat data
        s.graph.read(jsonData);
        
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
        
        // Fungsi untuk mendapatkan semua jenis koneksi
        function getConnectedNodes(nodeId) {{
            const connectedNodes = {{
                mutual: [],
                incoming: [],
                outgoing: []
            }};
            
            // Cari mutual connections (dua arah)
            s.graph.nodes().forEach(otherNode => {{
                if (otherNode.id !== nodeId) {{
                    const hasOutgoing = s.graph.hasEdge(nodeId, otherNode.id);
                    const hasIncoming = s.graph.hasEdge(otherNode.id, nodeId);
                    if (hasOutgoing && hasIncoming) {{
                        connectedNodes.mutual.push(otherNode.id);
                    }} else if (hasIncoming) {{
                        connectedNodes.incoming.push(otherNode.id);
                    }} else if (hasOutgoing) {{
                        connectedNodes.outgoing.push(otherNode.id);
                    }}
                }}
            }});
            
            return connectedNodes;
        }}
        
        // Fungsi untuk menampilkan panel koneksi
        function showConnectionsPanel(node, connections) {{
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
            
            // Tampilkan mutual connections
            if (connections.mutual.length > 0) {{
                const section = document.createElement('div');
                section.className = 'connection-section';
                section.innerHTML = `
                    <div class="connection-header mutual-header">Mutual (${{connections.mutual.length}})</div>
                    <div class="connection-names" id="mutual-names"></div>
                `;
                connectionsContainer.appendChild(section);
                
                connections.mutual.forEach(nodeId => {{
                    const neighbor = s.graph.nodes(nodeId);
                    if (neighbor) {{
                        const nameItem = document.createElement('span');
                        nameItem.className = 'name-item mutual-name';
                        nameItem.textContent = neighbor.label || neighbor.id;
                        nameItem.addEventListener('click', () => {{
                            s.camera.goTo({{ x: neighbor.x, y: neighbor.y, ratio: 0.8 }});
                        }});
                        document.getElementById('mutual-names').appendChild(nameItem);
                    }}
                }});
            }}
            
            // Tampilkan incoming connections
            if (connections.incoming.length > 0) {{
                const section = document.createElement('div');
                section.className = 'connection-section';
                section.innerHTML = `
                    <div class="connection-header incoming-header">Incoming (${{connections.incoming.length}})</div>
                    <div class="connection-names" id="incoming-names"></div>
                `;
                connectionsContainer.appendChild(section);
                
                connections.incoming.forEach(nodeId => {{
                    const neighbor = s.graph.nodes(nodeId);
                    if (neighbor) {{
                        const nameItem = document.createElement('span');
                        nameItem.className = 'name-item incoming-name';
                        nameItem.textContent = neighbor.label || neighbor.id;
                        nameItem.addEventListener('click', () => {{
                            s.camera.goTo({{ x: neighbor.x, y: neighbor.y, ratio: 0.8 }});
                        }});
                        document.getElementById('incoming-names').appendChild(nameItem);
                    }}
                }});
            }}
            
            // Tampilkan outgoing connections
            if (connections.outgoing.length > 0) {{
                const section = document.createElement('div');
                section.className = 'connection-section';
                section.innerHTML = `
                    <div class="connection-header outgoing-header">Outgoing (${{connections.outgoing.length}})</div>
                    <div class="connection-names" id="outgoing-names"></div>
                `;
                connectionsContainer.appendChild(section);
                
                connections.outgoing.forEach(nodeId => {{
                    const neighbor = s.graph.nodes(nodeId);
                    if (neighbor) {{
                        const nameItem = document.createElement('span');
                        nameItem.className = 'name-item outgoing-name';
                        nameItem.textContent = neighbor.label || neighbor.id;
                        nameItem.addEventListener('click', () => {{
                            s.camera.goTo({{ x: neighbor.x, y: neighbor.y, ratio: 0.8 }});
                        }});
                        document.getElementById('outgoing-names').appendChild(nameItem);
                    }}
                }});
            }}
            
            panel.style.display = 'block';
        }}
        
        // Fungsi untuk highlight node yang terhubung
        function highlightConnectedNodes(nodeId, connections) {{
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
            
            // Tampilkan node yang terhubung dengan warna berbeda
            connections.mutual.forEach(otherNodeId => {{
                const neighbor = s.graph.nodes(otherNodeId);
                if (neighbor) {{
                    neighbor.hidden = false;
                    neighbor.color = '#9467bd'; // Ungu untuk mutual
                }}
            }});
            
            connections.incoming.forEach(otherNodeId => {{
                const neighbor = s.graph.nodes(otherNodeId);
                if (neighbor) {{
                    neighbor.hidden = false;
                    neighbor.color = '#2ca02c'; // Hijau untuk incoming
                }}
            }});
            
            connections.outgoing.forEach(otherNodeId => {{
                const neighbor = s.graph.nodes(otherNodeId);
                if (neighbor) {{
                    neighbor.hidden = false;
                    neighbor.color = '#ff7f0e'; // Oranye untuk outgoing
                }}
            }});
            
            s.refresh();
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
            const connections = getConnectedNodes(node.id);
            showConnectionsPanel(node, connections);
            highlightConnectedNodes(node.id, connections);
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
   - Daftar node yang terhubung (Mutual, Incoming, Outgoing)
   - Hanya node yang terhubung yang akan ditampilkan di grafik
2. **Klik Nama di Daftar**: Klik nama node di daftar koneksi untuk fokus ke node tersebut
3. **Klik Area Kosong**: Kembalikan tampilan ke semua node
4. **Drag Node**: Klik dan tahan node untuk memindahkannya
5. **Zoom**: Gunakan scroll mouse untuk zoom in/out

### Legenda Warna:
- **Merah**: Node yang sedang dipilih
- **Ungu**: Mutual connections (dua arah)
- **Hijau**: Incoming connections (mengarah ke node yang dipilih)
- **Oranye**: Outgoing connections (dituju dari node yang dipilih)
- **Biru**: Node biasa

### Informasi Teknis:
- **Jumlah Node**: 855  # Diubah dari {len(data_json_content.get('nodes', []))} menjadi nilai tetap 855
- **Jumlah Edge**: {len(data_json_content.get('edges', []))}
""")
