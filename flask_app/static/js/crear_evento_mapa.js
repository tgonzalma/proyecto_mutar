let map;
let geocoder;
let marker;

async function initCrearEventoMap() {
    const { Map } = await google.maps.importLibrary("maps");
    await google.maps.importLibrary("marker");

    map = new Map(document.getElementById("mapa-preview"), {
        center: { lat: 40.4168, lng: -3.7038 },
        zoom: 12,
        mapId: window.GOOGLE_MAPS_MAP_ID || "DEMO_MAP_ID"
    });

    geocoder = new google.maps.Geocoder();

    const botonValidar = document.getElementById("validar-direccion");
    const inputUbicacion = document.getElementById("ubicacion");
    const inputCiudad = document.getElementById("ciudad");
    const inputLatitud = document.getElementById("latitud");
    const inputLongitud = document.getElementById("longitud");
    const estadoMapa = document.getElementById("estado-mapa");

    botonValidar.addEventListener("click", function () {
        const ubicacion = inputUbicacion.value.trim();
        const ciudad = inputCiudad ? inputCiudad.value.trim() : "";

        const direccionCompleta = ciudad
            ? `${ubicacion}, ${ciudad}`
            : ubicacion;

        if (!direccionCompleta) {
            estadoMapa.textContent = "Escribe una ubicación antes de validar.";
            return;
        }

        geocoder.geocode({ address: direccionCompleta }, (results, status) => {
    console.log("Dirección enviada:", direccionCompleta);
    console.log("Geocoder status:", status);
    console.log("Resultados:", results);

    if (status === "OK" && results[0]) {
        const location = results[0].geometry.location;
        const lat = location.lat();
        const lng = location.lng();

        inputLatitud.value = lat;
        inputLongitud.value = lng;

        map.setCenter({ lat, lng });
        map.setZoom(15);

        if (marker) {
            marker.setMap(null);
        }

        marker = new google.maps.Marker({
            map: map,
            position: { lat, lng },
            title: direccionCompleta
        });

        estadoMapa.textContent = "Dirección validada correctamente.";
    } else {
        inputLatitud.value = "";
        inputLongitud.value = "";
        estadoMapa.textContent = `No se pudo localizar esa dirección. Estado: ${status}`;
    }
});
    });
}