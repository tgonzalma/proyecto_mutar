function initMapaEventos() {
    console.log("ENTRO A initMapaEventos");

    const contenedorMapa = document.getElementById("mapa-eventos");
    console.log("CONTENEDOR MAPA:", contenedorMapa);

    if (!contenedorMapa) {
        console.error('No existe el div con id="mapa-eventos"');
        return;
    }

    const eventosScript = document.getElementById("eventos-data");
    let eventos = [];

    if (eventosScript) {
        try {
            eventos = JSON.parse(eventosScript.textContent);
        } catch (error) {
            console.error("Error parseando eventos-data:", error);
        }
    }

    console.log("EVENTOS:", eventos);

    const centroInicial = eventos.length
        ? {
            lat: parseFloat(eventos[0].latitud),
            lng: parseFloat(eventos[0].longitud)
        }
        : { lat: 40.4168, lng: -3.7038 };

    const map = new google.maps.Map(contenedorMapa, {
        center: centroInicial,
        zoom: eventos.length ? 12 : 6,
        mapId: window.GOOGLE_MAPS_MAP_ID || "DEMO_MAP_ID"
    });

    eventos.forEach((evento) => {
        const lat = parseFloat(evento.latitud);
        const lng = parseFloat(evento.longitud);

        if (!isNaN(lat) && !isNaN(lng)) {
            const marker = new google.maps.Marker({
                map: map,
                position: { lat, lng },
                title: evento.nombre
            });

            const infoWindow = new google.maps.InfoWindow({
                content: `
                    <div>
                        <h3>${evento.nombre || ""}</h3>
                        <p>${evento.ubicacion || ""}</p>
                        <p>${evento.ciudad || ""}</p>
                    </div>
                `
            });

            marker.addListener("click", () => {
                infoWindow.open({
                    anchor: marker,
                    map
                });
            });
        }
    });
}

window.initMapaEventos = initMapaEventos;