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
        background: rgba(255, 255, 255, 0.8);
        padding: 15px;
        border-radius: 8px;
        z-index: 100;
        max-height: 80%;
        overflow-y: auto;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        width: 280px; /* Lebar panel utama */
    }}
    #maintitle, #title, #titletext, #legend, #search, #attributeselect {{ margin-bottom: 10px; }}
    h2 {{ margin-top: 0; font-size: 1.2em; color: #333; }}
    a {{ text-decoration: none; color: #007bff; }}
    a:hover {{ text-decoration: underline; }}
    .cf::after {{ content: ""; display: table; clear: both; }} /* Clearfix */

    /* Node Attributes Panel */
    #node-attributes-panel {{
        position: absolute;
        top: 20px;
        left: 320px; /* Posisikan di sebelah kanan mainpanel */
        background: rgba(255, 255, 255, 0.9);
        padding: 15px;
        border-radius: 8px;
        z-index: 90; /* Sedikit di bawah mainpanel */
        max-height: 80%;
        overflow-y: auto;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        width: 300px; /* Lebar panel atribut node */
        display: none; /* Sembunyikan secara default */
        border-left: 1px solid #ccc; /* Pemisah visual */
    }}
    #node-attributes-panel h3 {{
        margin-top: 0;
        color: #333;
    }}
    #node-attributes-panel dl {{
        margin: 0;
        padding: 0;
    }}
    #node-attributes-panel dt {{
        font-weight: bold;
        margin-top: 8px;
        color: #555;
    }}
    #node-attributes-panel dd {{
        margin-left: 0;
        margin-bottom: 5px;
        padding-left: 10px;
        border-left: 3px solid #007bff;
    }}
    #node-attributes-panel .connections-list ul {{
        list-style-type: none;
        padding: 0;
    }}
    #node-attributes-panel .connections-list li {{
        margin-bottom: 3px;
        padding: 2px 0;
    }}


    #zoom {{
        position: absolute;
        bottom: 20px;
        right: 20px;
        z-index: 100;
        background: rgba(255, 255, 255, 0.8);
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
        bottom: 60px; /* Adjust position to not overlap with zoom */
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
                        <dt class="node">Node</dt>
                        <dd>Mewakili entitas</dd>
                        <dt class="edge">Edge</dt>
                        <dd>Mewakili koneksi</dd>
                        <dt class="colours">Warna</dt>
                        <dd>Menunjukkan kelompok yang berbeda</dd>
                    </dl>
                </div>
            </div>
            <div class="b1">
                <form>
                    <div id="search" class="cf"><h2>Cari:</h2>
                        <input type="text" name="search" value="Cari berdasarkan nama" class="empty"/><div class="state"></div>
                        <div class="results"></div>
                    </div>
                    <div class="cf" id="attributeselect"><h2>Pemilih Grup:</h2>
                        <div class="select">Pilih Grup</div>
                        <div class="list cf"></div>
                    </div>
                </form>
            </div>
        </div>
        <div id="information" style="display: none;">
            <h3>Informasi tentang Visualisasi</h3>
            <p>Ini adalah placeholder untuk informasi terperinci tentang visualisasi jaringan. Dalam HTML asli, konten ini akan dimuat atau diperluas secara dinamis melalui Fancybox.</p>
            <p>Jaringan menampilkan node dan edge dengan atribut seperti degree, centrality, dan inferred class. Node diwarnai berdasarkan kelas yang disimpulkan, dan ukurannya dapat mencerminkan metrik seperti PageRank atau degree.</p>
            <p>Gunakan bilah pencarian untuk menemukan node tertentu, dan pemilih grup untuk memfilter berdasarkan atribut. Perbesar/perkecil menggunakan kontrol atau roda mouse, dan geser dengan menyeret jaringan.</p>
            <p>Mengklik node mungkin mengungkapkan informasi lebih rinci di panel atribut (jika diimplementasikan sepenuhnya).</p>
        </div>
    </div>

    <div id="node-attributes-panel">
        <h3>Atribut Node: <span id="node-label"></span></h3>
        <dl id="node-details"></dl>
        <div class="connections-list">
            <h4>Connections:</h4>
            <ul id="connected-nodes-list"></ul>
        </div>
    </div>

    <div id="zoom">
        <div class="z" rel="in"><span>+</span></div>
        <div class="z" rel="out"><span>-</span></div>
        <div class="z" rel="center"><span>◎</span></div>
    </div>
    <div id="copyright">
        <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/3.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/3.0/88x31.png" /></a>
    </div>
    <div id="developercontainer">
        <a href="http://www.oii.ox.ac.uk" title="Oxford Internet Institute"><div id="oii"><span>OII</span></div></a>
        <a href="http://jisc.ac.uk" title="JISC"><div id="jisc"><span>JISC</span></div></a>
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
            var connectedNodesList = document.getElementById('connected-nodes-list');

            if (typeof sigma !== 'undefined') {{
                try {{
                    s = new sigma({{
                        container: container,
                        settings: {{
                            minNodeSize: 0.5,
                            maxNodeSize: 5,
                            minEdgeSize: 0.2,
                            maxEdgeSize: 0.5,
                            enableCamera: true, // Pastikan ini true
                            zoomMin: 0.1,
                            zoomMax: 10,
                            mouseEnabled: true, // Pastikan ini true
                            touchEnabled: true, // Pastikan ini true
                            doubleClickEnabled: false,
                            labelThreshold: 8,
                            autoRescale: false, // Penting untuk interaksi manual, matikan auto-rescale
                            // renderer: {{ // Tambahkan ini jika ada masalah rendering
                            //     container: document.getElementById('sigma-canvas'),
                            //     type: 'canvas'
                            // }}
                        }}
                    }});

                    console.log("Instansi Sigma dibuat.");

                    s.graph.read(jsonData);
                    console.log("Data grafik dimuat. Node:", s.graph.nodes().length, "Edge:", s.graph.edges().length);

                    s.refresh();
                    console.log("Grafik Sigma diperbarui.");

                    // Fungsionalitas zoom dan pusat dasar
                    document.querySelector('#zoom .z[rel="in"]').addEventListener('click', function() {{
                        s.camera.goTo({{ratio: s.camera.ratio / 1.5}});
                    }});
                    document.querySelector('#zoom .z[rel="out"]').addEventListener('click', function() {{
                        s.camera.goTo({{ratio: s.camera.ratio * 1.5}});
                    }});
                    document.querySelector('#zoom .z[rel="center"]').addEventListener('click', function() {{
                        s.camera.goTo({{x: 0, y: 0, ratio: 1}});
                    }});

                    // Inisialisasi Fancybox
                    if (typeof $.fn.fancybox === 'function') {{
                        $(".line.fb").fancybox({{
                            'autoDimensions': false,
                            'width': 600,
                            'height': 'auto',
                            'transitionIn': 'none',
                            'transitionOut': 'none',
                            'type': 'inline',
                            'href': '#information'
                        }});
                        console.log("Fancybox diinisialisasi.");
                    }} else {{
                        console.warn("Fancybox tidak dimuat. Tautan 'Informasi lebih lanjut' tidak akan berfungsi seperti yang diharapkan.");
                    }}

                    // Fungsionalitas pencarian
                    var searchInput = document.querySelector('#search input[name="search"]');
                    if (searchInput) {{
                        searchInput.addEventListener('input', function() {{
                            var query = this.value.toLowerCase();
                            s.graph.nodes().forEach(function(n) {{
                                if (query === '' || (n.label && n.label.toLowerCase().includes(query))) {{
                                    n.hidden = false;
                                }} else {{
                                    n.hidden = true;
                                }}
                            }});
                            s.refresh();
                            // Sembunyikan panel atribut saat pencarian baru
                            nodeAttributesPanel.style.display = 'none';
                        }});
                        console.log("Pendengar acara input pencarian ditambahkan.");
                    }}

                    // === Fungsionalitas Baru: Klik Node untuk Menampilkan Atribut dan Koneksi ===
                    s.bind('clickNode', function(e) {{
                        var node = e.data.node;
                        var nodeId = node.id;
                        console.log("Node diklik:", node.label || node.id);

                        // === Tampilkan Atribut Node ===
                        nodeAttributesPanel.style.display = 'block';
                        nodeLabelSpan.textContent = node.label || node.id;
                        nodeDetailsDl.innerHTML = '';
                        var attributesToShow = node.attributes || node;

                        for (var key in attributesToShow) {{
                            if (attributesToShow.hasOwnProperty(key)) {{
                                if (key === 'x' || key === 'y' || key === 'size' || key === 'color' || key === 'id' || key === 'label') {{
                                    continue;
                                }}
                                var dt = document.createElement('dt');
                                dt.textContent = key.replace(/([A-Z])/g, ' $1').replace(/^./, function(str){{ return str.toUpperCase(); }});
                                var dd = document.createElement('dd');
                                dd.textContent = attributesToShow[key];
                                nodeDetailsDl.appendChild(dt);
                                nodeDetailsDl.appendChild(dd);
                            }}
                        }}

                        // === Tampilkan Koneksi (Neighbors) ===
                        connectedNodesList.innerHTML = ''; // Bersihkan daftar koneksi sebelumnya
                        var connectedNodes = [];
                        var nodesToDisplay = {}; // Untuk menyimpan node yang harus ditampilkan (node yang diklik + tetangga)
                        var edgesToDisplay = {}; // Untuk menyimpan edge yang harus ditampilkan (edge yang terhubung)

                        // Tambahkan node yang diklik ke daftar yang akan ditampilkan
                        nodesToDisplay[nodeId] = true;

                        s.graph.edges().forEach(function(edge) {{
                            if (edge.source === nodeId) {{
                                // Jika edge dimulai dari node yang diklik
                                var targetNode = s.graph.nodes(edge.target);
                                if (targetNode) {{
                                    connectedNodes.push(targetNode.label || targetNode.id);
                                    nodesToDisplay[targetNode.id] = true;
                                    edgesToDisplay[edge.id] = true;
                                }}_
                            }} else if (edge.target === nodeId) {{
                                // Jika edge berakhir di node yang diklik
                                var sourceNode = s.graph.nodes(edge.source);
                                if (sourceNode) {{
                                    connectedNodes.push(sourceNode.label || sourceNode.id);
                                    nodesToDisplay[sourceNode.id] = true;
                                    edgesToDisplay[edge.id] = true;
                                }}
                            }}
                        }});

                        connectedNodes.forEach(function(neighborLabel) {{
                            var li = document.createElement('li');
                            li.textContent = neighborLabel;
                            connectedNodesList.appendChild(li);
                        }});

                        // === Saring Tampilan Grafik (Hanya Node yang Diklik + Tetangga yang Terlihat) ===
                        s.graph.nodes().forEach(function(n) {{
                            n.hidden = !nodesToDisplay[n.id];
                        }});
                        s.graph.edges().forEach(function(e) {{
                            e.hidden = !edgesToDisplay[e.id];
                        }});
                        s.refresh(); // Penting: segarkan grafik setelah menyembunyikan/menampilkan
                    }});

                    // Menyembunyikan panel atribut dan mengembalikan semua node/edge saat mengklik ruang kosong
                    s.bind('clickStage', function(e) {{
                        console.log("Klik di area kosong.");
                        nodeAttributesPanel.style.display = 'none';

                        // Tampilkan kembali semua node dan edge
                        s.graph.nodes().forEach(function(n) {{
                            n.hidden = false;
                        }});
                        s.graph.edges().forEach(function(e) {{
                            e.hidden = false;
                        }});
                        s.refresh();
                    }});

                } catch (e) {{
                    console.error("Kesalahan saat menginisialisasi Sigma.js:", e);
                }}
            }} else {{
                console.error("Pustaka Sigma.js tidak dimuat atau 'sigma' tidak terdefinisi. Harap periksa tautan CDN.");
            }}
        }});
    </script>
</body>
</html>
"""

st.set_page_config(layout="wide")
st.title("Contoh Visualisasi Jaringan OII (Streamlit)")

st.write("""
Ini adalah adaptasi Streamlit dari visualisasi jaringan HTML yang disediakan.
Data grafik dari `data.json` telah berhasil dimuat dan disematkan.
""")

# Render komponen HTML
components.html(html_code, height=800, scrolling=True)

st.info("""
**Instruksi dan Pemecahan Masalah:**

1.  **Coba Lagi:** Jalankan aplikasi Streamlit dengan kode yang diperbarui ini.
2.  **Cari Node:** Gunakan bilah pencarian untuk mencari "TinmasIndonesia" (atau node lain yang ingin Anda eksplorasi).
3.  **Klik Node:** Setelah node "TinmasIndonesia" terlihat, **klik langsung pada node tersebut** di area grafik.
    * Sebuah panel di sebelah kiri akan muncul, menampilkan atribut node.
    * Sekarang, grafik juga seharusnya hanya menampilkan node "TinmasIndonesia" dan semua node serta edge yang terhubung langsung dengannya.
    * Daftar "Connections" akan muncul di panel atribut, mencantumkan label node yang terhubung.
4.  **Gerakkan Grafik:** Coba seret area kosong di grafik (bukan node) untuk menggeser (pan) tampilan. Coba juga gulir roda mouse untuk memperbesar/memperkecil.

**Jika masih ada masalah, Lakukan Hal Ini:**

* **Buka Konsol Pengembang (Developer Console):** Ini adalah alat paling penting.
    * Tekan `F12` di browser Anda (atau klik kanan pada halaman dan pilih "Inspect" / "Periksa").
    * Buka tab "Console" (Konsol).
    * Cari pesan error berwarna merah.
    * Cari juga pesan `console.log` yang saya tambahkan. Ini akan memberi tahu kita apakah event klik terdeteksi dan apakah ada kesalahan saat mencoba menampilkan atribut atau menyaring grafik.
* **Periksa Struktur `data.json` Anda:**
    * Pastikan ada `edges` (koneksi) yang valid di `data.json` Anda yang menghubungkan node-node. Jika tidak ada edge yang relevan, fungsionalitas "Connections" tidak akan menampilkan apa pun.
    * Pastikan setiap edge memiliki properti `source` dan `target` yang mengacu pada `id` node yang ada.
* **Perhatikan Pengaturan Sigma.js `autoRescale`:** Saya telah menambahkan `autoRescale: false`. Terkadang, auto-rescale dapat mengganggu interaksi manual atau zoom. Jika masih tidak bisa digerakkan, coba komentar `autoRescale: false` atau ubah nilainya.
* **Bagikan Output Konsol:** Jika Anda melihat pesan error atau pesan `console.log` yang tidak terduga, salin dan tempelkan di sini. Ini akan sangat membantu dalam mendiagnosis masalah.
""")
