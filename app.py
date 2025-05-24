import streamlit as st
import streamlit.components.v1 as components
import json

# Muat data dari data.json
try:
    with open('data.json', 'r') as f:
        data_json_content = json.load(f)
except FileNotFoundError:
    st.error("Kesalahan: data.json tidak ditemukan. Pastikan file berada di direktori yang sama.")
    st.stop() # Hentikan eksekusi jika file data tidak ditemukan

# Konversi kamus Python ke string JSON untuk disematkan di JavaScript
json_data_str = json.dumps(data_json_content)

# HTML dan JavaScript code to embed in Streamlit
html_code = f"""
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en-gb" lang="en" xmlns:og="http://opengraphprotocol.org/schema/" xmlns:fb="http://www.facebook.com/2008/fbml" itemscope itemtype="http://schema.org/Map">

<head>
<title>Contoh Visualisasi Jaringan OII</title>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,height=device-height,initial-scale=1,user-scalable=no" />
<meta http-equiv="X-UA-Compatible" content="IE=Edge" />

<style>
    /* Basic styling to make the canvas visible, adapted from original CSS */
    body {{ margin: 0; overflow: hidden; font-family: sans-serif; }}
    .sigma-parent {{ position: absolute; width: 100%; height: 100%; top: 0; left: 0; }}
    .sigma-expand {{ position: absolute; width: 100%; height: 100%; top: 0; left: 0; }}

    /* Main panel on the left for controls and info */
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
    #maintitle, #title, #titletext, #legend, #search, #attributeselect {{ margin-bottom: 10px; }}
    h2 {{ margin-top: 0; font-size: 1.2em; color: #333; }}
    a {{ text-decoration: none; color: #007bff; }}
    a:hover {{ text-decoration: underline; }}
    .cf::after {{ content: ""; display: table; clear: both; }}

    /* Node Attributes Panel */
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
        border: 1px solid #ddd;
    }}
    #node-attributes-panel h3 {{
        margin-top: 0;
        color: #333;
        border-bottom: 1px solid #eee;
        padding-bottom: 8px;
    }}
    #node-attributes-panel dl {{
        margin: 0;
        padding: 0;
    }}
    #node-attributes-panel dt {{
        font-weight: bold;
        margin-top: 10px;
        color: #555;
    }}
    #node-attributes-panel dd {{
        margin-left: 0;
        margin-bottom: 8px;
        padding-left: 10px;
        border-left: 3px solid #007bff;
        word-break: break-word;
    }}
    #node-connections {{
        margin-top: 15px;
        padding-top: 10px;
        border-top: 1px dashed #ccc;
    }}
    .connection-item {{
        margin-bottom: 5px;
        padding: 5px;
        background: #f5f5f5;
        border-radius: 3px;
    }}

    #zoom {{
        position: absolute;
        bottom: 20px;
        right: 20px;
        z-index: 100;
        background: rgba(255, 255, 255, 0.9);
        padding: 5px;
        border-radius: 5px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }}
    #zoom .z {{
        width: 30px;
        height: 30px;
        line-height: 30px;
        text-align: center;
        border: 1px solid #ccc;
        cursor: pointer;
        margin: 5px;
        display: inline-block;
        border-radius: 3px;
        font-weight: bold;
        color: #555;
    }}
    #zoom .z:hover {{
        background-color: #eee;
    }}
    #copyright, #developercontainer {{
        position: absolute;
        bottom: 20px;
        left: 20px;
        font-size: 0.8em;
        color: #777;
        z-index: 100;
    }}
    #developercontainer {{
        left: auto;
        right: 20px;
        bottom: 60px;
    }}
    #oii, #jisc {{
        display: inline-block;
        margin-left: 10px;
        padding: 5px 10px;
        background-color: #f8f8f8;
        border: 1px solid #ddd;
        border-radius: 3px;
    }}
</style>

<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/sigma.js/1.2.1/sigma.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/sigma.js/1.2.1/plugins/sigma.parsers.json.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/sigma.js/1.2.1/plugins/sigma.renderers.customShapes.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/fancybox/2.1.5/jquery.fancybox.pack.js"></script>

</head>

<body>
    <div class="sigma-parent">
        <div class="sigma-expand" id="sigma-canvas" style="background-color: #f0f0f0;"></div>
    </div>
    <div id="mainpanel">
        <div class="col">
            <div id="maintitle"><h2>Visualisasi Jaringan OII</h2></div>
            <div id="title"></div>
            <div id="titletext">Ini adalah contoh visualisasi jaringan.</div>
            <div class="info cf">
                <dl>
                    <dt class="moreinformation"></dt>
                    <dd class="line"><a href="#information" class="line fb">Informasi lebih lanjut tentang visualisasi ini</a></dd>
                </dl>
            </div>
            <div id="legend">
                <div class="box">
                    <h2>Legenda:</h2>
                    <dl>
                        <dt style="color: #1f77b4;">Node</dt>
                        <dd>Mewakili entitas</dd>
                        <dt style="color: #999;">Edge</dt>
                        <dd>Mewakili koneksi</dd>
                        <dt class="colours">Warna</dt>
                        <dd>Menunjukkan kelompok yang berbeda</dd>
                    </dl>
                </div>
            </div>
            <div class="b1">
                <form>
                    <div id="search" class="cf"><h2>Cari:</h2>
                        <input type="text" name="search" value="" placeholder="Cari berdasarkan nama" class="empty"/>
                        <div class="state"></div>
                        <div class="results"></div>
                    </div>
                </form>
            </div>
        </div>
        <div id="information" style="display: none;">
            <h3>Informasi tentang Visualisasi</h3>
            <p>Visualisasi jaringan ini menampilkan hubungan antara berbagai entitas.</p>
            <p>Klik pada node untuk melihat detail dan koneksinya.</p>
        </div>
    </div>

    <div id="node-attributes-panel">
        <h3>Atribut Node: <span id="node-label"></span></h3>
        <dl id="node-details"></dl>
        <div id="node-connections">
            <h4>Koneksi:</h4>
            <div id="connections-list"></div>
        </div>
    </div>

    <div id="zoom">
        <div class="z" rel="in" title="Perbesar"><span>+</span></div>
        <div class="z" rel="out" title="Perkecil"><span>-</span></div>
        <div class="z" rel="center" title="Pusatkan"><span>◎</span></div>
        <div class="z" rel="reset" title="Reset Zoom"><span>↻</span></div>
    </div>
    <div id="copyright">
        <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/3.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/3.0/88x31.png" /></a>
    </div>

    <script type="text/javascript">
        // Sematkan data JSON secara langsung
        var jsonData = {json_data_str};

        // Inisialisasi Sigma.js saat DOM siap
        document.addEventListener('DOMContentLoaded', function() {{
            console.log("Konten DOM Dimuat. Menginisialisasi Sigma.js...");
            var s;
            var container = document.getElementById('sigma-canvas');
            var nodeAttributesPanel = document.getElementById('node-attributes-panel');
            var nodeLabelSpan = document.getElementById('node-label');
            var nodeDetailsDl = document.getElementById('node-details');
            var connectionsList = document.getElementById('connections-list');

            if (typeof sigma !== 'undefined') {{
                try {{
                    // Konfigurasi Sigma.js
                    s = new sigma({{
                        container: container,
                        settings: {{
                            minNodeSize: 3,
                            maxNodeSize: 15,
                            minEdgeSize: 0.5,
                            maxEdgeSize: 2,
                            enableCamera: true,
                            zoomMin: 0.05,
                            zoomMax: 20,
                            mouseEnabled: true,
                            touchEnabled: true,
                            doubleClickEnabled: true,
                            labelThreshold: 5,
                            defaultLabelSize: 14,
                            labelSize: 'proportional',
                            labelSizeRatio: 1,
                            drawLabels: true,
                            mouseWheelEnabled: true,
                            sideMargin: 2
                        }}
                    }});

                    console.log("Instansi Sigma dibuat.");

                    // Muat data grafik
                    s.graph.read(jsonData);
                    console.log("Data grafik dimuat. Node:", s.graph.nodes().length, "Edge:", s.graph.edges().length);

                    // Hitung ukuran node berdasarkan degree jika tidak ada ukuran yang ditentukan
                    s.graph.nodes().forEach(function(node) {{
                        if (!node.size) {{
                            node.size = Math.log(s.graph.degree(node.id) + 1;
                        }}
                        if (!node.color) {{
                            node.color = '#1f77b4';
                        }}
                        if (!node.label && node.attributes && node.attributes.name) {{
                            node.label = node.attributes.name;
                        }}
                    }});

                    // Atur warna edge jika tidak ada
                    s.graph.edges().forEach(function(edge) {{
                        if (!edge.color) {{
                            edge.color = '#999';
                        }}
                    }});

                    s.refresh();
                    console.log("Grafik Sigma diperbarui.");

                    // Fungsionalitas zoom
                    document.querySelector('#zoom .z[rel="in"]').addEventListener('click', function() {{
                        s.camera.goTo({{ ratio: s.camera.ratio / 1.5 }});
                    }});
                    document.querySelector('#zoom .z[rel="out"]').addEventListener('click', function() {{
                        s.camera.goTo({{ ratio: s.camera.ratio * 1.5 }});
                    }});
                    document.querySelector('#zoom .z[rel="center"]').addEventListener('click', function() {{
                        s.camera.goTo({{ x: 0, y: 0, ratio: 1 }});
                    }});
                    document.querySelector('#zoom .z[rel="reset"]').addEventListener('click', function() {{
                        s.camera.goTo({{ x: 0, y: 0, ratio: 1, angle: 0 }});
                    }});

                    // Fungsionalitas pencarian
                    var searchInput = document.querySelector('#search input[name="search"]');
                    if (searchInput) {{
                        searchInput.addEventListener('input', function() {{
                            var query = this.value.toLowerCase().trim();
                            s.graph.nodes().forEach(function(n) {{
                                var label = n.label || n.id || '';
                                if (query === '' || label.toLowerCase().includes(query)) {{
                                    n.hidden = false;
                                    n.color = n.originalColor || '#1f77b4';
                                }} else {{
                                    n.hidden = true;
                                }}
                            }});
                            s.refresh();
                        }});
                    }}

                    // Fungsi untuk menampilkan detail node dan koneksinya
                    function showNodeDetails(node) {{
                        // Tampilkan panel atribut
                        nodeAttributesPanel.style.display = 'block';

                        // Perbarui label node di panel
                        nodeLabelSpan.textContent = node.label || node.id || node.attributes?.name || 'Node ' + node.id;

                        // Bersihkan detail sebelumnya
                        nodeDetailsDl.innerHTML = '';
                        connectionsList.innerHTML = '';

                        // Tampilkan atribut node
                        var attributesToShow = node.attributes || node;
                        var excludedProps = ['x', 'y', 'size', 'color', 'id', 'label', 'hidden', 'originalColor'];

                        for (var key in attributesToShow) {{
                            if (attributesToShow.hasOwnProperty(key) && !excludedProps.includes(key)) {{
                                var dt = document.createElement('dt');
                                dt.textContent = key.replace(/([A-Z])/g, ' $1').replace(/^./, function(str){{ 
                                    return str.toUpperCase(); 
                                }});
                                
                                var dd = document.createElement('dd');
                                var value = attributesToShow[key];
                                dd.textContent = (value !== null && value !== undefined) ? value.toString() : 'N/A';
                                nodeDetailsDl.appendChild(dt);
                                nodeDetailsDl.appendChild(dd);
                            }}
                        }}

                        // Tampilkan koneksi node
                        var connectedNodes = [];
                        var connectedEdges = s.graph.edges().filter(function(edge) {{
                            return edge.source === node.id || edge.target === node.id;
                        }});

                        connectedEdges.forEach(function(edge) {{
                            var otherNodeId = edge.source === node.id ? edge.target : edge.source;
                            var otherNode = s.graph.nodes(otherNodeId);
                            if (otherNode) {{
                                connectedNodes.push(otherNode);
                                
                                var connectionItem = document.createElement('div');
                                connectionItem.className = 'connection-item';
                                
                                var direction = edge.source === node.id ? '→' : '←';
                                if (edge.source === edge.target) direction = '↔';
                                
                                connectionItem.innerHTML = `
                                    <strong>${{direction}} ${{otherNode.label || otherNode.id || 'Node ' + otherNode.id}}</strong>
                                    ${{edge.attributes?.type || edge.type || ''}}
                                `;
                                
                                connectionItem.style.cursor = 'pointer';
                                connectionItem.addEventListener('click', function() {{
                                    // Fokus ke node yang terhubung
                                    s.camera.goTo({{
                                        x: otherNode.x,
                                        y: otherNode.y,
                                        ratio: 0.5
                                    }});
                                    
                                    // Highlight node yang terhubung
                                    s.graph.nodes().forEach(function(n) {{
                                        n.color = n.originalColor || '#1f77b4';
                                    }});
                                    otherNode.originalColor = otherNode.color;
                                    otherNode.color = '#ff7f0e';
                                    s.refresh();
                                }});
                                
                                connectionsList.appendChild(connectionItem);
                            }}
                        }});

                        // Highlight node yang sedang dilihat
                        s.graph.nodes().forEach(function(n) {{
                            n.color = n.originalColor || '#1f77b4';
                        }});
                        node.originalColor = node.color;
                        node.color = '#d62728';
                        s.refresh();
                    }}

                    // Event klik node
                    s.bind('clickNode', function(e) {{
                        console.log("Node diklik:", e.data.node);
                        showNodeDetails(e.data.node);
                    }});

                    // Event double click node untuk zoom
                    s.bind('doubleClickNode', function(e) {{
                        var node = e.data.node;
                        s.camera.goTo({{
                            x: node.x,
                            y: node.y,
                            ratio: 0.5
                        }});
                    }});

                    // Menyembunyikan panel atribut saat mengklik area kosong
                    s.bind('clickStage', function(e) {{
                        nodeAttributesPanel.style.display = 'none';
                        
                        // Kembalikan warna node ke semula
                        s.graph.nodes().forEach(function(n) {{
                            if (n.originalColor) {{
                                n.color = n.originalColor;
                                delete n.originalColor;
                            }}
                        }});
                        s.refresh();
                    }});

                    // Enable drag and drop
                    s.bind('downNodes', function(e) {{
                        var node = e.data.nodes[0];
                        node.isDragging = true;
                    }});

                    s.bind('mouseup', function(e) {{
                        s.graph.nodes().forEach(function(n) {{
                            n.isDragging = false;
                        }});
                    }});

                    s.bind('mousemove', function(e) {{
                        var draggedNode = s.graph.nodes().find(function(n) {{
                            return n.isDragging;
                        }});
                        
                        if (draggedNode) {{
                            draggedNode.x = e.data.captor.x;
                            draggedNode.y = e.data.captor.y;
                            s.refresh();
                        }}
                    }});

                }} catch (e) {{
                    console.error("Kesalahan saat menginisialisasi Sigma.js:", e);
                    alert("Terjadi kesalahan saat memuat visualisasi. Lihat konsol untuk detail.");
                }}
            }} else {{
                console.error("Pustaka Sigma.js tidak dimuat atau 'sigma' tidak terdefinisi.");
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
components.html(html_code, height=800, scrolling=True)

st.markdown("""
### Panduan Penggunaan:
1. **Pencarian Node**: Gunakan kotak pencarian di panel kiri untuk mencari node tertentu
2. **Klik Node**: Klik pada node untuk melihat detail atribut dan koneksinya di panel kanan
3. **Zoom**: 
   - Gunakan tombol + dan - di pojok kanan bawah 
   - Atau gunakan scroll mouse
4. **Drag Node**: Klik dan tahan node untuk memindahkannya
5. **Double Click**: Double klik pada node untuk zoom ke node tersebut

### Informasi Teknis:
- **Jumlah Node**: {num_nodes}
- **Jumlah Edge**: {num_edges}
""".format(
    num_nodes=len(data_json_content.get('nodes', [])),
    num_edges=len(data_json_content.get('edges', []))
))
