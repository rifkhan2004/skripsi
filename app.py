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
        /* (Keep other CSS styles the same as before) */
        .connection-type {{
            display: inline-block;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 0.8em;
            font-weight: bold;
            margin-left: 5px;
        }}
        .out-connection {{
            background-color: #ffebee;
            color: #d32f2f;
            border: 1px solid #d32f2f;
        }}
        .in-connection {{
            background-color: #e8f5e9;
            color: #2e7d32;
            border: 1px solid #2e7d32;
        }}
        .bidirectional-connection {{
            background-color: #e3f2fd;
            color: #1565c0;
            border: 1px solid #1565c0;
        }}
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/sigma.js/1.2.1/sigma.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/sigma.js/1.2.1/plugins/sigma.parsers.json.min.js"></script>
</head>
<body>
    <!-- (Keep HTML structure the same as before) -->
    <script>
        // (Keep previous JavaScript code until the connection display part)
        
        // Fungsi untuk menentukan jenis koneksi
        function getConnectionType(sourceId, targetId) {{
            const edgesFromSource = s.graph.edges().filter(e => e.source === sourceId && e.target === targetId);
            const edgesFromTarget = s.graph.edges().filter(e => e.source === targetId && e.target === sourceId);
            
            if (edgesFromSource.length > 0 && edgesFromTarget.length > 0) {{
                return {{
                    type: 'bidirectional',
                    symbol: '↔',
                    text: 'Dua Arah',
                    class: 'bidirectional-connection'
                }};
            }} else if (edgesFromSource.length > 0) {{
                return {{
                    type: 'out',
                    symbol: '→',
                    text: 'Keluar',
                    class: 'out-connection'
                }};
            }} else if (edgesFromTarget.length > 0) {{
                return {{
                    type: 'in',
                    symbol: '←',
                    text: 'Masuk',
                    class: 'in-connection'
                }};
            }}
            return {{
                type: 'unknown',
                symbol: '',
                text: 'Tidak diketahui',
                class: ''
            }};
        }}

        // Fungsi tampilkan detail node (updated connection display)
        s.bind('clickNode', function(e) {{
            const node = e.data.node;
            // ... (keep previous code until connections display)
            
            // Tampilkan daftar node yang terhubung dengan informasi jenis koneksi
            connectedNodeIds.forEach(nodeId => {{
                const connectedNode = s.graph.nodes(nodeId);
                if (connectedNode) {{
                    const connectionItem = document.createElement('div');
                    connectionItem.className = 'connection-item';
                    
                    // Tentukan jenis koneksi
                    const connection = getConnectionType(node.id, connectedNode.id);
                    
                    // Header dengan nama node dan info koneksi
                    const header = document.createElement('div');
                    header.className = 'connection-header';
                    
                    const nameSpan = document.createElement('span');
                    nameSpan.className = 'connection-name';
                    nameSpan.textContent = connectedNode.label || connectedNode.id;
                    
                    const directionSpan = document.createElement('span');
                    directionSpan.className = 'connection-direction';
                    directionSpan.textContent = connection.symbol;
                    directionSpan.title = connection.text;
                    
                    const typeBadge = document.createElement('span');
                    typeBadge.className = `connection-type ${{connection.class}}`;
                    typeBadge.textContent = connection.text;
                    
                    header.appendChild(nameSpan);
                    header.appendChild(directionSpan);
                    header.appendChild(typeBadge);
                    
                    // Statistik degree dengan penekanan visual
                    const stats = document.createElement('div');
                    stats.className = 'connection-stats';
                    
                    // Out-degree dengan highlight jika ini out-connection
                    const outDegree = document.createElement('div');
                    outDegree.className = 'stat-item';
                    if (connection.type === 'out' || connection.type === 'bidirectional') {{
                        outDegree.innerHTML = '<span class="stat-label">➔ Out:</span> <span class="out-degree"><strong>' + (connectedNode.outDegree || 0) + '</strong></span>';
                    }} else {{
                        outDegree.innerHTML = '<span class="stat-label">Out:</span> <span class="out-degree">' + (connectedNode.outDegree || 0) + '</span>';
                    }}
                    
                    // In-degree dengan highlight jika ini in-connection
                    const inDegree = document.createElement('div');
                    inDegree.className = 'stat-item';
                    if (connection.type === 'in' || connection.type === 'bidirectional') {{
                        inDegree.innerHTML = '<span class="stat-label">← In:</span> <span class="in-degree"><strong>' + (connectedNode.inDegree || 0) + '</strong></span>';
                    }} else {{
                        inDegree.innerHTML = '<span class="stat-label">In:</span> <span class="in-degree">' + (connectedNode.inDegree || 0) + '</span>';
                    }}
                    
                    // Total degree
                    const totalDegree = document.createElement('div');
                    totalDegree.className = 'stat-item';
                    totalDegree.innerHTML = '<span class="stat-label">∑ Total:</span> <span class="total-degree">' + (connectedNode.degree || 0) + '</span>';
                    
                    stats.appendChild(outDegree);
                    stats.appendChild(inDegree);
                    stats.appendChild(totalDegree);
                    
                    // Gabungkan semua elemen
                    connectionItem.appendChild(header);
                    connectionItem.appendChild(stats);
                    
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
        
        // (Keep the rest of the JavaScript code the same)
    </script>
</body>
</html>
"""

st.set_page_config(layout="wide")
st.title("Visualisasi Jaringan Interaktif")

# (Keep the rest of the Streamlit code the same)
