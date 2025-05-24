import streamlit as st
import streamlit.components.v1 as components
import json

# Muat data dari data.json
try:
    with open('data.json', 'r') as f:
        data_json_content = json.load(f)
        
    # Validasi struktur data
    if 'nodes' not in data_json_content or 'edges' not in data_json_content:
        st.error("Struktur data.json tidak valid. Harus memiliki 'nodes' dan 'edges'")
        st.stop()
        
    st.success(f"Data berhasil dimuat: {len(data_json_content['nodes'])} node, {len(data_json_content['edges'])} edges")
    
except FileNotFoundError:
    st.error("Kesalahan: data.json tidak ditemukan. Pastikan file berada di direktori yang sama.")
    st.stop()
except json.JSONDecodeError:
    st.error("Kesalahan: data.json tidak valid. Periksa format JSON.")
    st.stop()

# Debug: Tampilkan contoh data
with st.expander("Lihat contoh data.json"):
    st.json(data_json_content["nodes"][:2] if len(data_json_content["nodes"]) > 0 else {})
    st.json(data_json_content["edges"][:2] if len(data_json_content["edges"]) > 0 else {})

# Konversi kamus Python ke string JSON untuk disematkan di JavaScript
json_data_str = json.dumps(data_json_content)

# HTML dan JavaScript code to embed in Streamlit
html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Visualisasi Jaringan</title>
    <meta charset="utf-8">
    <style>
        body {{ margin: 0; padding: 0; overflow: hidden; }}
        #sigma-container {{
            width: 100%;
            height: 800px;
            background-color: #f0f0f0;
            position: relative;
        }}
        #loading {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-family: sans-serif;
            color: #666;
        }}
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/sigma.js/1.2.1/sigma.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/sigma.js/1.2.1/plugins/sigma.parsers.json.min.js"></script>
</head>
<body>
    <div id="sigma-container">
        <div id="loading">Memuat visualisasi jaringan...</div>
    </div>

    <script>
        // Debug info
        console.log("Memulai inisialisasi Sigma.js");
        
        // Data jaringan
        const jsonData = {json_data_str};
        console.log("Data JSON yang diterima:", jsonData);
        
        // Validasi data sebelum memuat
        if (!jsonData.nodes || jsonData.nodes.length === 0) {{
            console.error("Tidak ada node dalam data");
            document.getElementById('loading').textContent = "Error: Tidak ada node dalam data";
            throw new Error("Tidak ada node dalam data");
        }}
        
        // Inisialisasi sigma
        try {{
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
                    defaultNodeColor: '#1f77b4',
                    defaultEdgeColor: '#999'
                }}
            }});
            
            console.log("Sigma instance dibuat");
            
            // Muat data
            s.graph.read(jsonData);
            console.log("Data dimuat:", s.graph.nodes().length, "nodes,", s.graph.edges().length, "edges");
            
            // Pastikan semua node memiliki koordinat
            s.graph.nodes().forEach(node => {{
                if (typeof node.x === 'undefined' || typeof node.y === 'undefined') {{
                    // Jika tidak ada koordinat, beri nilai acak
                    node.x = Math.random();
                    node.y = Math.random();
                    console.warn("Node", node.id, "tidak memiliki koordinat, menggunakan nilai acak");
                }}
                
                // Set default properties jika tidak ada
                if (!node.size) node.size = 5;
                if (!node.color) node.color = s.settings('defaultNodeColor');
                if (!node.label) node.label = node.id;
            }});
            
            // Set default properties untuk edge
            s.graph.edges().forEach(edge => {{
                if (!edge.color) edge.color = s.settings('defaultEdgeColor');
                if (!edge.size) edge.size = 1;
            }});
            
            // Hitung layout jika tidak ada posisi
            if (s.graph.nodes().some(n => typeof n.x === 'undefined')) {{
                console.log("Menghitung layout menggunakan forceAtlas2");
                sigma.layouts.forceAtlas2.start(s, {{
                    adjustSizes: true,
                    scalingRatio: 10,
                    gravity: 0.2
                }});
                
                // Stop layout setelah 3 detik
                setTimeout(() => sigma.layouts.forceAtlas2.stop(s), 3000);
            }}
            
            // Refresh tampilan
            s.refresh();
            console.log("Grafik direfresh");
            
            // Sembunyikan loading
            document.getElementById('loading').style.display = 'none';
            
        }} catch (error) {{
            console.error("Error saat memuat grafik:", error);
            document.getElementById('loading').textContent = "Error: " + error.message;
        }}
    </script>
</body>
</html>
"""

st.set_page_config(layout="wide")
st.title("Visualisasi Jaringan Interaktif")

# Render komponen HTML
components.html(html_code, height=850)

# Debug informasi
st.markdown(f"""
### Informasi Debug:
- **Jumlah Node**: {len(data_json_content.get('nodes', []))}
- **Jumlah Edge**: {len(data_json_content.get('edges', []))}
- **Node Contoh**: 
  ```json
  {json.dumps(data_json_content.get('nodes', [{}])[0]) if data_json_content.get('nodes') else 'Tidak ada node'}
