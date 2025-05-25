import streamlit as st
import streamlit.components.v1 as components
import json

# Muat data dari data.json
try:
    with open('data.json', 'r') as f:
        data_json_content = json.load(f)
except FileNotFoundError:
    st.error("Error: File data.json tidak ditemukan. Pastikan file berada di direktori yang sama.")
    st.stop()

# Konversi ke string JSON untuk JavaScript
json_data_str = json.dumps(data_json_content)

# Kode HTML dan JavaScript
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
        #panel-utama {{
            position: absolute;
            top: 20px;
            left: 20px;
            background: rgba(255, 255, 255, 0.9);
            padding: 15px;
            border-radius: 8px;
            z-index: 100;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            width: 280px;
        }}
        #panel-info {{
            position: absolute;
            top: 20px;
            right: 20px;
            background: rgba(255, 255, 255, 0.95);
            padding: 15px;
            border-radius: 8px;
            z-index: 90;
            max-height: 80vh;
            overflow-y: auto;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            width: 300px;
            display: none;
        }}
        .baris-metrik {{
            margin-bottom: 10px;
            padding-bottom: 10px;
            border-bottom: 1px solid #eee;
        }}
        .label-metrik {{
            font-weight: bold;
            color: #555;
        }}
        .nilai-metrik {{
            color: #333;
        }}
        .judul-bagian {{
            font-weight: bold;
            margin: 15px 0 5px 0;
            color: #444;
        }}
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/sigma.js/1.2.1/sigma.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/sigma.js/1.2.1/plugins/sigma.parsers.json.min.js"></script>
</head>
<body>
    <div id="sigma-container"></div>
    <div id="panel-utama">
        <h2>Visualisasi Jaringan</h2>
        <p>Klik pada node untuk melihat informasi detail.</p>
    </div>
    <div id="panel-info">
        <h3 id="judul-node">Informasi Node</h3>
        <div id="metrik-node"></div>
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
        
        // Fungsi untuk menampilkan panel info node
        function tampilkanPanelInfo(node) {{
            const panel = document.getElementById('panel-info');
            const judul = document.getElementById('judul-node');
            const kontainerMetrik = document.getElementById('metrik-node');
            
            judul.textContent = node.label || node.id;
            kontainerMetrik.innerHTML = '';
            
            const atribut = node.attributes || {{}};
            
            // Daftar metrik yang akan ditampilkan
            const daftarMetrik = [
                {{ key: 'out_degree', label: 'Out-Degree' }},
                {{ key: 'in_degree', label: 'In-Degree' }},
                {{ key: 'closeness_centrality', label: 'Closeness Centrality' }},
                {{ key: 'inferred_class', label: 'Kelas' }},
                {{ key: 'eigenvector_centrality', label: 'Eigenvector Centrality' }},
                {{ key: 'weighted_in_degree', label: 'Weighted In-Degree' }},
                {{ key: 'betweenness_centrality', label: 'Betweenness Centrality' }},
                {{ key: 'pagerank', label: 'PageRank' }},
                {{ key: 'harmonic_closeness', label: 'Harmonic Closeness' }},
                {{ key: 'weighted_degree', label: 'Weighted Degree' }},
                {{ key: 'weighted_out_degree', label: 'Weighted Out-Degree' }}
            ];
            
            // Buat tampilan metrik
            daftarMetrik.forEach(metrik => {{
                if (atribut[metrik.key] !== undefined) {{
                    const baris = document.createElement('div');
                    baris.className = 'baris-metrik';
                    baris.innerHTML = `
                        <div class="label-metrik">${{metrik.label}}:</div>
                        <div class="nilai-metrik">${{atribut[metrik.key]}}</div>
                    `;
                    kontainerMetrik.appendChild(baris);
                }}
            }});
            
            panel.style.display = 'block';
        }}
        
        // Event klik node
        s.bind('clickNode', function(e) {{
            const node = e.data.node;
            tampilkanPanelInfo(node);
            
            // Highlight node yang diklik
            s.graph.nodes().forEach(n => {{
                n.color = n.id === node.id ? '#d62728' : '#1f77b4';
            }});
            s.refresh();
        }});
        
        // Event klik latar untuk menyembunyikan panel
        s.bind('clickStage', function() {{
            document.getElementById('panel-info').style.display = 'none';
            
            // Reset warna node
            s.graph.nodes().forEach(n => {{
                n.color = '#1f77b4';
            }});
            s.refresh();
        }});
    </script>
</body>
</html>
"""

st.set_page_config(layout="wide")
st.title("Visualisasi Jaringan Interaktif")

# Render komponen HTML
components.html(html_code, height=850)

st.markdown(f"""
### Panduan Penggunaan:
1. **Klik Node**: Klik pada node untuk melihat informasi detail
2. **Klik Latar**: Klik area kosong untuk menyembunyikan panel info
3. **Zoom**: Gunakan scroll mouse untuk memperbesar/memperkecil
4. **Geser**: Klik dan drag untuk menggeser tampilan

### Informasi Teknis:
- **Jumlah Node**: {len(data_json_content.get('nodes', []))}
- **Jumlah Edge**: {len(data_json_content.get('edges', []))}
""")
