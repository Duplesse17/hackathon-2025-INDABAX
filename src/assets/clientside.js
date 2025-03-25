// Charge la librairie html2pdf.js (via CDN)
// 1. Charger html2canvas d'abord
var html2canvasScript = document.createElement('script');
html2canvasScript.src = 'https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js';
html2canvasScript.onload = function() {
    console.log('html2canvas est chargé !');

    // 2. Ensuite charger html2pdf
    var html2pdfScript = document.createElement('script');
    html2pdfScript.src = 'https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js';
    html2pdfScript.onload = function() {
        console.log('html2pdf est chargé !');
    };

    document.head.appendChild(html2pdfScript);
};

document.head.appendChild(html2canvasScript);
;

// Dash clientside callback
window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        download_pdf: function(n_clicks) {
            if (!n_clicks) {
                return window.dash_clientside.no_update;
            }

            if (typeof html2pdf === 'undefined' || typeof html2canvas === 'undefined') {
                alert('Les scripts ne sont pas encore chargés !');
                return window.dash_clientside.no_update;
            }

            alert('Export en PDF lancé !');

            var element = document.getElementById('pdf-content');
            var btn = document.getElementById('btn-pdf');

            if (!element) {
                alert('Contenu à exporter non trouvé !');
                return window.dash_clientside.no_update;
            }

            if (btn) btn.style.display = 'none';

            var opt = {
                margin: 0.5,
                filename: 'dashboard_donneurs.pdf',
                image: { type: 'jpeg', quality: 0.98 },
                html2canvas: { scale: 2, useCORS: true },
                jsPDF: { unit: 'in', format: 'a4', orientation: 'portrait' }
            };

            function generatePDF(mapElement) {
                html2canvas(mapElement, { useCORS: true, scale: 2 }).then(canvas => {
                    console.log('Canvas créé !');
                    var imgData = canvas.toDataURL("image/png");

                    // Crée une image à partir du canvas
                    var img = new Image();
                    img.src = imgData;
                    img.style.width = "100%";
                    img.style.marginBottom = "20px";

                    // Remplacer temporairement la carte par l'image capturée
                    mapElement.innerHTML = "";
                    mapElement.appendChild(img);

                    // Générer le PDF
                    html2pdf().set(opt).from(element).save().then(() => {
                        if (btn) btn.style.display = 'block';
                        alert('Export en PDF terminé !');
                        window.location.reload();
                    });
                }).catch(error => {
                    console.error("Erreur lors de la capture avec html2canvas:", error);
                    alert("Erreur lors de la capture de la carte.");
                    if (btn) btn.style.display = 'block';
                });
            }

            // Attend que l'élément soit dispo dans le DOM
            function waitForElement(id, callback) {
                const interval = setInterval(() => {
                    const el = document.getElementById(id);
                    if (el) {
                        clearInterval(interval);
                        callback(el);
                    }
                }, 100);
            }

            waitForElement('map-donateurs', generatePDF);

            return '';
        }
    }
});
