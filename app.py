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

# Kode HTML dan JavaScript untuk disematkan di Streamlit
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
    /* Styling dasar untuk membuat kanvas terlihat, diadaptasi dari CSS asli */
    body {{ margin: 0; overflow: hidden; font-family: sans-serif; }}
    .sigma-parent {{ position: absolute; width: 100%; height: 100%; top: 0; left: 0; }}
    .sigma-expand {{ position: absolute; width: 100%; height: 100%; top: 0; left: 0; }}
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
    }}
    #maintitle, #title, #titletext, #legend, #search, #attributeselect {{ margin-bottom: 10px; }}
    h2 {{ margin-top: 0; font-size: 1.2em; color: #333; }}
    a {{ text-decoration: none; color: #007bff; }}
    a:hover {{ text-decoration: underline; }}
    .cf::after {{ content: ""; display: table; clear: both; }} /* Clearfix */
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
        bottom: 60px; /* Sesuaikan posisi agar tidak tumpang tindih dengan zoom */
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

            if (typeof sigma !== 'undefined') {{
                try {{
                    s = new sigma({{
                        container: container,
                        settings: {{
                            minNodeSize: 0.5,
                            maxNodeSize: 5,
                            minEdgeSize: 0.2,
                            maxEdgeSize: 0.5,
                            // Aktifkan roda mouse untuk zoom
                            enableCamera: true,
                            zoomMin: 0.1,
                            zoomMax: 10,
                            mouseEnabled: true, // Aktifkan interaksi mouse (pan, zoom)
                            touchEnabled: true, // Aktifkan interaksi sentuh
                            doubleClickEnabled: false, // Nonaktifkan zoom klik ganda
                            labelThreshold: 8 // Hanya tampilkan label untuk node yang lebih besar dari ini
                        }}
                    }});

                    console.log("Instansi Sigma dibuat.");

                    // Baca data grafik secara manual
                    s.graph.read(jsonData);
                    console.log("Data grafik dimuat. Node:", s.graph.nodes().length, "Edge:", s.graph.edges().length);

                    // Segarkan grafik untuk menerapkan perubahan dan merender
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

                    // Inisialisasi Fancybox untuk tautan "Informasi lebih lanjut"
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

                    // Placeholder untuk fungsionalitas pencarian
                    var searchInput = document.querySelector('#search input[name="search"]');
                    var searchResults = document.querySelector('#search .results');
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
                        }});
                        console.log("Pendengar acara input pencarian ditambahkan.");
                    }}

                }} catch (e) {{
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
**Jika grafik tidak muncul, periksa langkah-langkah berikut:**

1.  **Buka Konsol Pengembang (Developer Console) di Browser Anda:**
    * Klik kanan pada halaman Streamlit Anda dan pilih "Inspect" (Periksa) atau "Inspect Element" (Periksa Elemen).
    * Buka tab "Console" (Konsol). Cari pesan error berwarna merah. Pesan ini akan memberikan petunjuk tentang masalah JavaScript.
    * Cari juga pesan `console.log` yang saya tambahkan (misalnya, "Instansi Sigma dibuat.", "Data grafik dimuat.", "Grafik Sigma diperbarui."). Ini akan menunjukkan sampai tahap mana inisialisasi Sigma.js berjalan.

2.  **Pastikan `data.json` ada:** Pastikan file `data.json` berada di direktori yang sama dengan skrip Streamlit Anda. Skrip Python akan mencoba membacanya.

3.  **Periksa Koneksi CDN:** Pastikan Anda memiliki koneksi internet aktif. Sigma.js dan jQuery dimuat dari CDN (Content Delivery Network). Jika koneksi buruk atau CDN tidak dapat dijangkau, pustaka tidak akan dimuat.

4.  **Isi Data `data.json`:** Pastikan file `data.json` Anda memiliki struktur yang benar dan data node dan edge yang valid. Terkadang, data yang kosong atau rusak dapat menyebabkan Sigma.js gagal merender.

5.  **Ukuran Node/Edge:** Jika `minNodeSize` dan `maxNodeSize` sangat kecil, node mungkin terlalu kecil untuk terlihat. Coba tingkatkan nilai ini untuk pengujian. Demikian juga dengan `minEdgeSize` dan `maxEdgeSize`.
    * Coba ubah `minNodeSize: 0.5, maxNodeSize: 5` menjadi `minNodeSize: 5, maxNodeSize: 20` untuk melihat apakah node menjadi terlihat lebih besar.

Dengan memeriksa konsol browser Anda, kita harus bisa menemukan akar masalah mengapa grafik tidak muncul.
""")
