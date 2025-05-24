import streamlit as st
import streamlit.components.v1 as components
import json

# The data from data.json, fetched in the previous step
data_json_content = {"nodes":[{"label":"keyboardxs","x":527.043212890625,"y":1121.2760009765625,"id":"378","attributes":{"Out-Degree":"1","In-Degree":"0","Closeness Centrality":"1.0","Inferred Class":"27","Degree":"1","Eigenvector Centrality":"0.0","Weighted In-Degree":"0.0","Betweenness Centrality":"0.0","PageRank":"4.4773350124840554E-4","Harmonic Closeness Centrality":"1.0","Weighted Degree":"1.0","Weighted Out-Degree":"1.0"},"color":"rgb(255,29,0)","size":10.520445823669434},{"label":"gggilang___","x":273.08087158203125,"y":225.0216064453125,"id":"127","attributes":{"Out-Degree":"1","In-Degree":"0","Closeness Centrality":"0.5555555555555556","Inferred Class":"27","Degree":"1","Eigenvector Centrality":"0.0","Weighted In-Degree":"0.0","Betweenness Centrality":"0.0","PageRank":"4.4773350124840554E-4","Harmonic Closeness Centrality":"0.6","Weighted Degree":"1.0","Weighted Out-Degree":"1.0"},"color":"rgb(255,29,0)","size":10.520445823669434},{"label":"audimaxell","x":-713.412109375,"y":861.30419921875,"id":"457","attributes":{"Out-Degree":"1","In-Degree":"0","Closeness Centrality":"0.42857142857142855","Inferred Class":"27","Degree":"1","Eigenvector Centrality":"0.0","Weighted In-Degree":"0.0","Betweenness Centrality":"0.0","PageRank":"4.4773350124840554E-4","Harmonic Closeness Centrality":"0.5","Weighted Degree":"1.0","Weighted Out-Degree":"1.0"},"color":"rgb(255,29,0)","size":10.520445823669434},{"label":"jawirtzz","x":1336.5831298828125,"y":375.06201171875,"id":"136","attributes":{"Out-Degree":"0","In-Degree":"1","Closeness Centrality":"0.0","Inferred Class":"14","Degree":"1","Eigenvector Centrality":"0.003306742811576341","Weighted In-Degree":"1.0","Betweenness Centrality":"0.0","PageRank":"8.28312481982923E-4","Harmonic Closeness Centrality":"0.0","Weighted Degree":"1.0","Weighted Out-Degree":"0.0"},"color":"rgb(255,29,0)","size":10.520445823669434},{"label":"zclittlesun","x":-1060.163330078125,"y":683.7406616210938,"id":"645","attributes":{"Out-Degree":"1","In-Degree":"0","Closeness Centrality":"1.0","Inferred Class":"79","Degree":"1","Eigenvector Centrality":"0.0","Weighted In-Degree":"0.0","Betweenness Centrality":"0.0","PageRank":"4.4773350124840554E-4","Harmonic Closeness Centrality":"1.0","Weighted Degree":"1.0","Weighted Out-Degree":"1.0"},"color":"rgb(255,29,0)","size":10.520445823669434},{"label":"yourbbypie","x":-1082.9017333984375,"y":91.91224670410156,"id":"442","attributes":{"Out-Degree":"1","In-Degree":"0","Closeness Centrality":"1.0","Inferred Class":"53","Degree":"1","Eigenvector Centrality":"0.0","Weighted In-Degree":"0.0","Betweenness Centrality":"0.0","PageRank":"4.4773350124840554E-4","Harmonic Closeness Centrality":"1.0","Weighted Degree":"1.0","Weighted Out-Degree":"1.0"},"color":"rgb(255,29,0)","size":10.520445823669434},{"label":"bogoroditsye","x":-118.03048706054688,"y":-860.6763916015625,"id":"70","attributes":{"Out-Degree":"0","In-Degree":"1","Closeness Centrality":"0.0","Inferred Class":"4","Degree":"1","Eigenvector Centrality":"0.003306742811576341","Weighted In-Degree":"1.0","Betweenness Centrality":"0.0","PageRank":"8.28312481982923E-4","Harmonic Closeness Centrality":"0.0","Weighted Degree":"1.0","Weighted Out-Degree":"0.0"},"color":"rgb(255,29,0)","size":10.520445823669434},{"label":"woodymolky48","x":691.913330078125,"y":982.612060546875,"id":"377","attributes":{"Out-Degree":"1","In-Degree":"0","Closeness Centrality":"1.0","Inferred Class":"27","Degree":"1","Eigenvector Centrality":"0.0","Weighted In-Degree":"0.0","Betweenness Centrality":"0.0","PageRank":"4.4773350124840554E-4","Harmonic Closeness Centrality":"1.0","Weighted Degree":"1.0","Weighted Out-Degree":"1.0"},"color":"rgb(255,29,0)","size":10.520445823669434},{"label":"raysanrr","x":28.192562103271484,"y":-578.7124633789062,"id":"573","attributes":{"Out-Degree":"1","In-Degree":"1","Closeness Centrality":"0.5555555555555556","Inferred Class":"27","Degree":"2","Eigenvector Centrality":"0.007322047778057521","Weighted In-Degree":"1.0","Betweenness Centrality":"0.0","PageRank":"7.23139767204085E-4","Harmonic Closeness Centrality":"0.6","Weighted Degree":"2.0","Weighted Out-Degree":"1.0"},"color":"rgb(255,0,207)","size":11.040891647338867},{"label":"sunbaemee","x":590.5667114257812,"y":-1057.0252685546875,"id":"539","attributes":{"Out-Degree":"1","In-Degree":"1","Closeness Centrality":"0.5","Inferred Class":"27","Degree":"2","Eigenvector Centrality":"0.004705342977795791","Weighted In-Degree":"1.0","Betweenness Centrality":"1.0930753675465923E-5","PageRank":"6.247483437259293E-4","Harmonic Closeness Centrality":"0.5833333333333333","Weighted Degree":"2.0","Weighted Out-Degree":"1.0"},"color":"rgb(255,0,207)","size":11.040891647338867},{"label":"lilujangkasep","x":140.07577514648438,"y":-447.42999267578125,"id":"231","attributes":{"Out-Degree":"1","In-Degree":"0","Closeness Centrality":"0.5555555555555556","Inferred Class":"27","Degree":"1","Eigenvector Centrality":"0.0","Weighted In-Degree":"0.0","Betweenness Centrality":"0.0","PageRank":"4.4773350124840554E-4","Harmonic Closeness Centrality":"0.6","Weighted Degree":"1.0","Weighted Out-Degree":"1.0"},"color":"rgb(255,29,0)","size":10.520445823669434},{"label":"NalarPolitik_","x":149.4954833984375,"y":-350.18975830078125,"id":"354","attributes":{"Out-Degree":"1","In-Degree":"0","Closeness Centrality":"0.5555555555555556","Inferred Class":"27","Degree":"1","Eigenvector Centrality":"0.0","Weighted In-Degree":"0.0","Betweenness Centrality":"0.0","PageRank":"4.4773350124840554E-4","Harmonic Closeness Centrality":"0.6","Weighted Degree":"1.0","Weighted Out-Degree":"1.0"},"color":"rgb(255,29,0)","size":10.520445823669434},{"label":"maulanarezaaa","x":-872.87158203125,"y":-1012.3003540039062,"id":"840","attributes":{"Out-Degree":"1","In-Degree":"0","Closeness Centrality":"1.0","Inferred Class":"128","Degree":"1","Eigenvector Centrality":"0.0","Weighted In-Degree":"0.0","Betweenness Centrality":"0.0","PageRank":"4.4773350124840554E-4","Harmonic Closeness Centrality":"1.0","Weighted Degree":"1.0","Weighted Out-Degree":"1.0"},"color":"rgb(255,29,0)","size":10.520445823669434},{"label":"garistengah_id","x":-715.7640380859375,"y":741.2252807617188,"id":"458","attributes":{"Out-Degree":"3","In-Degree":"8","Closeness Centrality":"0.625","Inferred Class":"27","Degree":"11","Eigenvector Centrality":"0.04743571858056197","Weighted In-Degree":"10.0","Betweenness Centrality":"6.831721047166202E-5","PageRank":"0.0028833719967933094","Harmonic Closeness Centrality":"0.7","Weighted Degree":"14.0","Weighted Out-Degree":"4.0"},"color":"rgb(158,11,0)","size":15.724906921386719},{"label":"Faried_qonaah","x":-163.38148498535156,"y":356.5648193359375,"id":"607","attributes":{"Out-Degree":"1","In-Degree":"0","Closeness Centrality":"0.5555555555555556","Inferred Class":"27","Degree":"1","Eigenvector Centrality":"0.0","Weighted In-Degree":"0.0","Betweenness Centrality":"0.0","PageRank":"4.4773350124840554E-4","Harmonic Closeness Centrality":"0.6","Weighted Degree":"1.0","Weighted Out-Degree":"1.0"},"color":"rgb(255,29,0)","size":10.520445823669434},{"label":"newpersonnnnn","x":-691.9506225585938,"y":-99.23341369628906,"id":"663","attributes":{"Out-Degree":"2","In-Degree":"1","Closeness Centrality":"0.5","Inferred Class":"27","Degree":"3","Eigenvector Centrality":"0.00935381156732835","Weighted In-Degree":"1.0","Betweenness Centrality":"0.0","PageRank":"8.685328090669927E-4","Harmonic Closeness Centrality":"0.5740740740740741","Weighted Degree":"4.0","Weighted Out-Degree":"3.0"},"color":"rgb(153,0,255)","size":11.561338424682617},{"label":"yudhabjnugroho","x":-499.29144287109375,"y":-986.4978637695312,"id":"731","attributes":{"Out-Degree":"1","In-Degree":"0","Closeness Centrality":"1.0","Inferred Class":"99","Degree":"1","Eigenvector Centrality":"0.0","Weighted In-Degree":"0.0","Betweenness Centrality":"0.0","PageRank":"4.4773350124840554E-4","Harmonic Closeness Centrality":"1.0","Weighted Degree":"1.0","Weighted Out-Degree":"1.0"},"color":"rgb(255,29,0)","size":10.520445823669434},{"label":"Leo_Nardi10","x":766.014404296875,"y":659.760009765625,"id":"113","attributes":{"Out-Degree":"1","In-Degree":"0","Closeness Centrality":"1.0","Inferred Class":"27","Degree":"1","Eigenvector Centrality":"0.0","Weighted In-Degree":"0.0","Betweenness Centrality":"0.0","PageRank":"4.4773350124840554E-4","Harmonic Closeness Centrality":"1.0","Weighted Degree":"1.0","Weighted Out-Degree":"1.0"},"color":"rgb(255,29,0)","size":10.520445823669434},{"label":"gilabola_ina","x":1152.066162109375,"y":212.08535766601562,"id":"76","attributes":{"Out-Degree":"0","In-Degree":"17","Closeness Centrality":"0.0","Inferred Class":"27","Degree":"17","Eigenvector Centrality":"0.0562146277967978","Weighted In-Degree":"20.0","Betweenness Centrality":"0.0","PageRank":"0.006361345355738598","Harmonic Closeness Centrality":"0.0","Weighted Degree":"20.0","Weighted Out-Degree":"0.0"},"color":"rgb(255,176,0)","size":18.847583770751953},{"label":"lyfesdgtrouble","x":-271.61920166015625,"y":-1094.3529052734375,"id":"851","attributes":{"Out-Degree":"1","In-Degree":"0","Closeness Centrality":"1.0","Inferred Class":"27","Degree":"1","Eigenvector Centrality":"0.0","Weighted In-Degree":"0.0","Betweenness Centrality":"0.0","PageRank":"4.4773350124840554E-4","Harmonic Closeness Centrality":"1.0","Weighted Degree":"1.0","Weighted Out-Degree":"1.0"},"color":"rgb(255,29,0)","size":10.520445823669434},{"label":"jayhilgers","x":194.76620483398438,"y":346.2784423828125,"id":"133","attributes":{"Out-Degree":"1","In-Degree":"0","Closeness Centrality":"0.5555555555555556","Inferred Class":"27","Degree":"1","Eigenvector Centrality":"0.0","Weighted In-Degree":"0.0","Betweenness Centrality":"0.0","PageRank":"4.4773350124840554E-4","Harmonic Closeness Centrality":"0.6","Weighted Degree":"1.0","Weighted Out-Degree":"1.0"},"color":"rgb(255,29,0)","size":10.520445823669434},{"label":"Bimbelia","x":-1272.7027587890625,"y":-299.666748046875,"id":"486","attributes":{"Out-Degree":"1","In-Degree":"0","Closeness Centrality":"0.3181818181818182","Inferred Class":"27","Degree":"1","Eigenvector Centrality":"0.0","Weighted In-Degree":"0.0","Betweenness Centrality":"0.0","PageRank":"4.4773350124840554E-4","Harmonic Closeness Centrality":"0.4047619047619047","Weighted Degree":"1.0","Weighted Out-Degree":"1.0"},"color":"rgb(255,29,0)","size":10.520445823669434},{"label":"Mako_Brimop","x":-374.48553466796875,"y":-6.061717987060547,"id":"153","attributes":{"Out-Degree":"1","In-Degree":"0","Closeness Centrality":"0.5555555555555556","Inferred Class":"27","Degree":"1","Eigenvector Centrality":"0.0","Weighted In-Degree":"0.0","Betweenness Centrality":"0.0","PageRank":"4.4773350124840554E-4","Harmonic Closeness Centrality":"0.6","Weighted Degree":"1.0","Weighted Out-Degree":"1.0"},"color":"rgb(255,29,0)","size":10.520445823669434},{"label":"gloriahermawan","x":762.1218872070312,"y":1000.2949829101562,"id":"303","attributes":{"Out-Degree":"1","In-Degree":"0","Closeness Centrality":"1.0","Inferred Class":"27","Degree":"1","Eigenvector Centrality":"0.0","Weighted In-Degree":"0.0","Betweenness Centrality":"0.0","PageRank":"4.4773350124840554E-4","Harmonic Closeness Centrality":"1.0","Weighted Degree":"1.0","Weighted Out-Degree":"1.0"},"color":"rgb(255,29,0)","size":10.520445823669434},{"label":"Indri9614838740","x":887.3236083984375,"y":441.0811462402344,"id":"561","attributes":{"Out-Degree":"2","In-Degree":"0","Closeness Centrality":"1.0","Inferred Class":"27","Degree":"2","Eigenvector Centrality":"0.0","Weighted In-Degree":"0.0","Betweenness Centrality":"0.0","PageRank":"4.4773350124840554E-4","Harmonic Closeness Centrality":"1.0","Weighted Degree":"2.0","Weighted Out-Degree":"2.0"},"color":"rgb(255,0,207)","size":11.040891647338867},{"label":"dianaanr","x":-187.801025390625,"y":-326.0653381347656,"id":"563","attributes":{"Out-Degree":"1","In-Degree":"0","Closeness Centrality":"0.5555555555555556","Inferred Class":"27","Degree":"1","Eigenvector Centrality":"0.0","Weighted In-Degree":"0.0","Betweenness Centrality":"0.0","PageRank":"4.4773350124840554E-4","Harmonic Closeness Centrality":"0.6","Weighted Degree":"1.0","Weighted Out-Degree":"1.0"},"color":"rgb(255,29,0)","size":10.520445823669434},{"label":"artix_id","x":293.31585693359375,"y":-1386.1551513671875,"id":"701","attributes":{"Out-Degree":"0","In-Degree":"1","Closeness Centrality":"0.0","Inferred Class":"91","Degree":"1","Eigenvector Centrality":"0.003306742811576341","Weighted In-Degree":"1.0","Betweenness Centrality":"0.0","PageRank":"8.28312481982923E-4","Harmonic Closeness Centrality":"0.0","Weighted Degree":"1.0","Weighted Out-Degree":"0.0"},"color":"rgb(255,29,0)","size":10.520445823669434},{"label":"wlfdeersh","x":-651.7702026367188,"y":617.375244140625,"id":"428","attributes":{"Out-Degree":"2","In-Degree":"2","Closeness Centrality":"0.4375","Inferred Class":"27","Degree":"4","Eigenvector Centrality":"0.011795104649539524","Weighted In-Degree":"2.0","Betweenness Centrality":"1.9128818932065367E-5","PageRank":"0.0010923012781023662","Harmonic Closeness Centrality":"0.5119047619047619","Weighted Degree":"6.0","Weighted Out-Degree":"4.0"},"color":"rgb(5,0,255)","size":12.08178424835205},{"label":"dwicn_","x":-133.1171875,"y":-438.3934020996094,"id":"625","attributes":{"Out-Degree":"1","In-Degree":"0","Closeness Centrality":"0.5555555555555556","Inferred Class":"27","Degree":"1","Eigenvector Centrality":"0.0","Weighted In-Degree":"0.0","Betweenness Centrality":"0.0","PageRank":"4.4773350124840554E-4","Harmonic Closeness Centrality":"0.6","Weighted Degree":"1.0","Weighted Out-Degree":"1.0"},"color":"rgb(255,29,0)","size":10.520445823669434},{"label":"wiyaah07","x":680.6908569335938,"y":-862.3262329101562,"id":"57","attributes":{"Out-Degree":"1","In-Degree":"0","Closeness Centrality":"0.5","Inferred Class":"27","Degree":"1","Eigenvector Centrality":"0.0","Weighted In-Degree":"0.0","Betweenness Centrality":"0.0","PageRank":"4.4773350124840554E-4","Harmonic Closeness Centrality":"0.5833333333333334","Weighted Degree":"1.0","Weighted Out-Degree":"1.0"},"color":"rgb(255,29,0)","size":10.520445823669434},{"label":"amaulr","x":477.6130065917969,"y":-259.22607421875,"id":"126","attributes":{"Out-Degree":"1","In-Degree":"0","Closeness Centrality":"0.5555555555555556","Inferred Class":"27","Degree":"1","Eigenvector Centrality":"0.0","Weighted In-Degree":"0.0","Betweenness Centrality":"0.0","PageRank":"4.4773350124840554E-4","Harmonic Closeness Centrality":"0.6","Weighted Degree":"1.0","Weighted Out-Degree":"1.0"},"color":"rgb(255,29,0)","size":10.520445823669434},{"label":"cbarcelonafans","x":-760.5227661132812,"y":957.822021484375,"id":"28","attributes":{"Out-Degree":"1","In-Degree":"0","Closeness Centrality":"1.0","Inferred Class":"1","Degree":"1","Eigenvector Centrality":"0.0","Weighted In-Degree":"0.0","Betweenness Centrality":"0.0","PageRank":"4.4773350124840554E-4","Harmonic Closeness Centrality":"1.0","Weighted Degree":"1.0","Weighted Out-Degree":"1.0"},"color":"rgb(255,29,0)","size":10.520445823669434},{"label":"andreirawan3218","x":-702.4229125976562,"y":-282.3051452636719,"id":"107","attributes":{"Out-Degree":"1","In-Degree":"0","Closeness Centrality":"0.5555555555555556","Inferred Class":"27","Degree":"1","Eigenvector Centrality":"0.0","Weighted In-Degree":"0.0","Betweenness Centrality":"0.0","PageRank":"4.4773350124840554E-4","Harmonic Closeness Centrality":"0.6","Weighted Degree":"1.0","Weighted Out-Degree":"1.0"},"color":"rgb(255,29,0)","size":10.520445823669434},{"label":"ballondor","x":-446.9725646972656,"y":-1106.5648193359375,"id":"732","attributes":{"Out-Degree":"0","In-Degree":"1","Closeness Centrality":"0.0","Inferred Class":"99","Degree":"1","Eigenvector Centrality":"0.003306742811576341","Weighted In-Degree":"1.0","Betweenness Centrality":"0.0","PageRank":"8.28312481982923E-4","Harmonic Closeness Centrality":"0.0","Weighted Degree":"1.0","Weighted Out-Degree":"0.0"},"color":"rgb(255,29,0)","size":10.520445823669434},{"label":"mzulkiflimz","x":-56.436973571777344,"y":-1443.380859375,"id":"565","attributes":{"Out-Degree":"0","In-Degree":"1","Closeness Centrality":"0.0","Inferred Class":"69","Degree":"1","Eigenvector Centrality":"0.003306742811576341","Weighted In-Degree":"1.0","Betweenness Centrality":"0.0","PageRank":"8.28312481982923E-4","Harmonic Closeness Centrality":"0.0","Weighted Degree":"1.0","Weighted Out-Degree":"0.0"},"color":"rgb(255,29,0)","size":10.520445823669434},{"label":"KakkoiRizal","x":1208.7066650390625,"y":138.55140686035156,"id":"275","attributes":{"Out-Degree":"1","In-Degree":"0","Closeness Centrality":"1.0","Inferred Class":"27","Degree":"1","Eigenvector Centrality":"0.0","Weighted In-Degree":"0.0","Betweenness Centrality":"0.0","PageRank":"4.4773350124840554E-4","Harmonic Closeness Centrality":"1.0","Weighted Degree":"1.0","Weighted Out-Degree":"1.0"},"color":"rgb(255,29,0)","size":10.520445823669434},{"label":"baby__potato","x":-72.1227798461914,"y":553.521484375,"id":"648","attributes":{"Out-Degree":"1","In-Degree":"0","Closeness Centrality":"0.5555555555555556","Inferred Class":"27","Degree":"1","Eigenvector Centrality":"0.0","Weighted In-Degree":"0.0","Betweenness Centrality":"0.0","PageRank":"4.4773350124840554E-4","Harmonic Closeness Centrality":"0.6","Weighted Degree":"1.0","Weighted Out-Degree":"1.0"},"color":"rgb(255,29,0)","size":10.520445823669434},{"label":"law_ismylife","x":-474.8955383300781,"y":1213.529052734375,"id":"698","attributes":{"Out-Degree":"0","In-Degree":"1","Closeness Centrality":"0.0","Inferred Class":"90","Degree":"1","Eigenvector Centrality":"0.003306742811576341","Weighted In-Degree":"1.0","Betweenness Centrality":"0.0","PageRank":"6.380229916156643E-4","Harmonic Closeness Centrality":"0.0","Weighted Degree":"1.0","Weighted Out-Degree":"0.0"},"color":"rgb(255,29,0)","size":10.520445823669434},{"label":"moonnliiighhttt","x":-1059.5399169921875,"y":612.2024536132812,"id":"646","attributes":{"Out-Degree":"0","In-Degree":"1","Closeness Centrality":"0.0","Inferred Class":"79","Degree":"1","Eigenvector Centrality":"0.003306742811576341","Weighted In-Degree":"1.0","Betweenness Centrality":"0.0","PageRank":"8.28312481982923E-4","Harmonic Closeness Centrality":"0.0","Weighted Degree":"1.0","Weighted Out-Degree":"0.0"},"color":"rgb(255,29,0)","size":10.520445823669434},{"label":"indikatorcoid","x":-792.8505859375,"y":-1031.4990234375,"id":"836","attributes":{"Out-Degree":"1","In-Degree":"1","Closeness Centrality":"0.0","Inferred Class":"126","Degree":"2","Eigenvector Centrality":"0.004705342977795791","Weighted In-Degree":"2.0","Betweenness Centrality":"0.0","PageRank":"4.4773350124840554E-4","Harmonic Closeness Centrality":"0.0","Weighted Degree":"4.0","Weighted Out-Degree":"2.0"},"color":"rgb(255,0,207)","size":11.040891647338867},{"label":"dearjeonv_","x":-775.7344970703125,"y":-876.6012573242188,"id":"121","attributes":{"Out-Degree":"1","In-Degree":"1","Closeness Centrality":"1.0","Inferred Class":"12","Degree":"2","Eigenvector Centrality":"0.004705342977795791","Weighted In-Degree":"1.0","Betweenness Centrality":"0.0","PageRank":"0.002984021746025338","Harmonic Closeness Centrality":"1.0","Weighted Degree":"2.0","Weighted Out-Degree":"1.0"},"color":"rgb(255,0,207)","size":11.040891647338867},{"label":"_AfsalMuhammad","x":-1060.1422119140625,"y":855.590087890625,"id":"661","attributes":{"Out-Degree":"1","In-Degree":"0","Closeness Centrality":"1.0","Inferred Class":"83","Degree":"1","Eigenvector Centrality":"0.0","Weighted In-Degree":"0.0","Betweenness Centrality":"0.0","PageRank":"4.4773350124840554E-4","Harmonic Closeness Centrality":"1.0","Weighted Degree":"1.0","Weighted Out-Degree":"1.0"},"color":"rgb(255,29,0)","size":10.520445823669434},{"label":"rioagustio_","x":286.7366638183594,"y":-829.2724609375,"id":"32","attributes":{"Out-Degree":"1","In-Degree":"0","Closeness Centrality":"0.5","Inferred Class":"27","Degree":"1","Eigenvector Centrality":"0.0","Weighted In-Degree":"0.0","Betweenness Centrality":"0.0","PageRank":"4.4773350124840554E-4","Harmonic Closeness Centrality":"0.5833333333333334","Weighted Degree":"1.0","Weighted Out-Degree":"1.0"},"color":"rgb(255,29,0)","size":10.520445823669434}],"edges":[{"source":"378","target":"136","id":"380","attributes":{},"color":"rgb(255,29,0)","size":1.0},{"source":"127","target":"136","id":"128","attributes":{},"color":"rgb(255,29,0)","size":1.0},{"source":"457","target":"458","id":"462","attributes":{},"color":"rgb(255,29,0)","size":1.0},{"source":"645","target":"646","id":"718","attributes":{},"color":"rgb(255,29,0)","size":1.0},{"source":"442","target":"76","id":"443","attributes":{},"color":"rgb(255,29,0)","size":1.0},{"source":"573","target":"70","id":"576","attributes":{},"color":"rgb(255,0,207)","size":1.0},{"source":"539","target":"57","id":"540","attributes":{},"color":"rgb(255,0,207)","size":1.0},{"source":"231","target":"573","id":"232","attributes":{},"color":"rgb(255,29,0)","size":1.0},{"source":"354","target":"563","id":"356","attributes":{},"color":"rgb(255,29,0)","size":1.0},{"source":"840","target":"836","id":"914","attributes":{},"color":"rgb(255,29,0)","size":1.0},{"source":"458","target":"76","id":"463","attributes":{},"color":"rgb(158,11,0)","size":1.0},{"source":"458","target":"243","id":"464","attributes":{},"color":"rgb(158,11,0)","size":1.0},{"source":"607","target":"458","id":"608","attributes":{},"color":"rgb(255,29,0)","size":1.0},{"source":"663","target":"428","id":"736","attributes":{},"color":"rgb(153,0,255)","size":1.0},{"source":"663","target":"76","id":"737","attributes":{},"color":"rgb(153,0,255)","size":1.0},{"source":"731","target":"732","id":"806","attributes":{},"color":"rgb(255,29,0)","size":1.0},{"source":"113","target":"458","id":"115","attributes":{},"color":"rgb(255,29,0)","size":1.0},{"source":"851","target":"836","id":"925","attributes":{},"color":"rgb(255,29,0)","size":1.0},{"source":"133","target":"127","id":"134","attributes":{},"color":"rgb(255,29,0)","size":1.0},{"source":"486","target":"76","id":"487","attributes":{},"color":"rgb(255,29,0)","size":1.0},{"source":"153","target":"428","id":"156","attributes":{},"color":"rgb(255,29,0)","size":1.0},{"source":"303","target":"76","id":"304","attributes":{},"color":"rgb(255,29,0)","size":1.0},{"source":"561","target":"76","id":"564","attributes":{},"color":"rgb(255,0,207)","size":1.0},{"source":"561","target":"458","id":"562","attributes":{},"color":"rgb(255,0,207)","size":1.0},{"source":"563","target":"354","id":"566","attributes":{},"color":"rgb(255,29,0)","size":1.0},{"source":"701","target":"836","id":"775","attributes":{},"color":"rgb(255,29,0)","size":1.0},{"source":"428","target":"663","id":"431","attributes":{},"color":"rgb(5,0,255)","size":1.0},{"source":"428","target":"153","id":"430","attributes":{},"color":"rgb(5,0,255)","size":1.0},{"source":"625","target":"573","id":"626","attributes":{},"color":"rgb(255,29,0)","size":1.0},{"source":"57","target":"539","id":"59","attributes":{},"color":"rgb(255,29,0)","size":1.0},{"source":"126","target":"136","id":"129","attributes":{},"color":"rgb(255,29,0)","size":1.0},{"source":"28","target":"76","id":"29","attributes":{},"color":"rgb(255,29,0)","size":1.0},{"source":"107","target":"428","id":"108","attributes":{},"color":"rgb(255,29,0)","size":1.0},{"source":"732","target":"731","id":"807","attributes":{},"color":"rgb(255,29,0)","size":1.0},{"source":"565","target":"836","id":"567","attributes":{},"color":"rgb(255,29,0)","size":1.0},{"source":"275","target":"76","id":"278","attributes":{},"color":"rgb(255,29,0)","size":1.0},{"source":"648","target":"458","id":"721","attributes":{},"color":"rgb(255,29,0)","size":1.0},{"source":"698","target":"458","id":"772","attributes":{},"color":"rgb(255,29,0)","size":1.0},{"source":"646","target":"645","id":"719","attributes":{},"color":"rgb(255,29,0)","size":1.0},{"source":"836","target":"840","id":"912","attributes":{},"color":"rgb(255,0,207)","size":1.0},{"source":"836","target":"851","id":"924","attributes":{},"color":"rgb(255,0,207)","size":1.0},{"source":"836","target":"565","id":"568","attributes":{},"color":"rgb(255,0,207)","size":1.0},{"source":"836","target":"701","id":"776","attributes":{},"color":"rgb(255,0,207)","size":1.0},{"source":"121","target":"76","id":"122","attributes":{},"color":"rgb(255,0,207)","size":1.0},{"source":"121","target":"836","id":"123","attributes":{},"color":"rgb(255,0,207)","size":1.0},{"source":"661","target":"458","id":"734","attributes":{},"color":"rgb(255,29,0)","size":1.0},{"source":"32","target":"836","id":"35","attributes":{},"color":"rgb(255,29,0)","size":1.0}]}


# Convert Python dict to JSON string for embedding in JavaScript
json_data_str = json.dumps(data_json_content)

# HTML and JavaScript code to embed in Streamlit
# Adjusted script loading order and used a more appropriate CDN for sigma.parseJson.js
html_code = f"""
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en-gb" lang="en" xmlns:og="http://opengraphprotocol.org/schema/" xmlns:fb="http://www.facebook.com/2008/fbml" itemscope itemtype="http://schema.org/Map">

<head>
<title>OII Network Visualisation Example</title>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,height=device-height,initial-scale=1,user-scalable=no" />
<meta http-equiv="X-UA-Compatible" content="IE=Edge" />

<style>
    /* Basic styling to make the canvas visible, adapted from original CSS */
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
<script src="https://cdnjs.cloudflare.com/ajax/libs/sigma.js/1.2.1/plugins/sigma.parsers.json.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/fancybox/2.1.5/jquery.fancybox.pack.js"></script>

</head>

<body>
    <div class="sigma-parent">
        <div class="sigma-expand" id="sigma-canvas" style="background-color: #f0f0f0;"></div>
    </div>
    <div id="mainpanel">
        <div class="col">
            <div id="maintitle"><h2>OII Network Visualisation</h2></div>
            <div id="title"></div>
            <div id="titletext">This is an example network visualization.</div>
            <div class="info cf">
                <dl>
                    <dt class="moreinformation"></dt>
                    <dd class="line"><a href="#information" class="line fb">More about this visualisation</a></dd>
                </dl>
            </div>
            <div id="legend">
                <div class="box">
                    <h2>Legend:</h2>
                    <dl>
                        <dt class="node">Node</dt>
                        <dd>Represents an entity</dd>
                        <dt class="edge">Edge</dt>
                        <dd>Represents a connection</dd>
                        <dt class="colours">Colours</dt>
                        <dd>Indicate different groups</dd>
                    </dl>
                </div>
            </div>
            <div class="b1">
                <form>
                    <div id="search" class="cf"><h2>Search:</h2>
                        <input type="text" name="search" value="Search by name" class="empty"/><div class="state"></div>
                        <div class="results"></div>
                    </div>
                    <div class="cf" id="attributeselect"><h2>Group Selector:</h2>
                        <div class="select">Select Group</div>
                        <div class="list cf"></div>
                    </div>
                </form>
            </div>
        </div>
        <div id="information" style="display: none;">
            <h3>Information about the Visualization</h3>
            <p>This is a placeholder for detailed information about the network visualization. In the original HTML, this content would be dynamically loaded or expanded via Fancybox.</p>
            <p>The network displays nodes and edges with attributes like degree, centrality, and inferred class. Nodes are colored based on their inferred class, and their size can reflect a metric like PageRank or degree.</p>
            <p>Use the search bar to find specific nodes, and the group selector to filter by attributes. Zoom in/out using the controls or mouse wheel, and pan by dragging the network.</p>
            <p>Clicking on a node might reveal more detailed information in an attribute pane (if implemented fully).</p>
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
        // Embed the JSON data directly
        var jsonData = {json_data_str};

        // Initialize Sigma.js
        var s;
        if (typeof sigma !== 'undefined') {{
            s = new sigma({{
                container: 'sigma-canvas',
                settings: {{
                    minNodeSize: 0.5,
                    maxNodeSize: 5,
                    minEdgeSize: 0.2,
                    maxEdgeSize: 0.5,
                    // Enable mouse wheel for zoom
                    enableCamera: true,
                    zoomMin: 0.1,
                    zoomMax: 10,
                    mouseEnabled: true, // Enable mouse interactions (pan, zoom)
                    touchEnabled: true, // Enable touch interactions
                    doubleClickEnabled: false // Disable double click zoom
                }}
            }});

            // Load the data using sigma.parsers.json (since the original used sigma.parseJson.js)
            // sigma.parsers.json expects a URL, but we have the data directly.
            // So we will manually read the graph data.
            s.graph.read(jsonData);

            // Refresh the graph to apply changes
            s.refresh();

            // Basic zoom and center functionality
            document.querySelector('#zoom .z[rel="in"]').addEventListener('click', function() {{
                s.camera.goTo({{ratio: s.camera.ratio / 1.5}});
            }});
            document.querySelector('#zoom .z[rel="out"]').addEventListener('click', function() {{
                s.camera.goTo({{ratio: s.camera.ratio * 1.5}});
            }});
            document.querySelector('#zoom .z[rel="center"]').addEventListener('click', function() {{
                s.camera.goTo({{x: 0, y: 0, ratio: 1}});
            }});

            // Initialize Fancybox for the "More information" link
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
            }} else {{
                console.warn("Fancybox not loaded. 'More information' link will not work as intended.");
            }}

            // Placeholder for search functionality (requires more complex JS)
            var searchInput = document.querySelector('#search input[name="search"]');
            var searchResults = document.querySelector('#search .results');
            if (searchInput) {{
                searchInput.addEventListener('input', function() {{
                    var query = this.value.toLowerCase();
                    s.graph.nodes().forEach(function(n) {{
                        if (query === '' || n.label.toLowerCase().includes(query)) {{
                            n.hidden = false;
                        }} else {{
                            n.hidden = true;
                        }}
                    }});
                    s.refresh();
                }});
            }}

        }} else {{
            console.error("Sigma.js library not loaded. Please check CDN links.");
        }}
    </script>
</body>
</html>
"""

st.set_page_config(layout="wide")
st.title("OII Network Visualisation Example (Streamlit)")

st.write("""
This is a Streamlit adaptation of the provided HTML network visualization.
The graph data from `data.json` has been successfully loaded and embedded.
""")

# Render the HTML component
components.html(html_code, height=800, scrolling=True)

st.info("""
**Note on functionality:**
This version addresses the `sigma.parsers is undefined` error by ensuring the correct loading order of Sigma.js and its JSON parser plugin from CDNs.
Basic interactive elements like zoom buttons and a placeholder search bar are included.
For advanced interactions (like the full search/filter logic from the original `main.js`) and complete styling,
you might still need to replicate or embed the exact content of the original JavaScript and CSS files,
as these CDNs provide generic library versions.
""")
