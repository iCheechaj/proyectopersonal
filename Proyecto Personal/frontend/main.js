//Trabajando logica del frontend
const API_URL = "http://127.0.0.1:5000/games/";


// UTILIDADES
async function fetchJson(url, options = {}) {
    try {
        const res = await fetch(url, options);
        // codigo 200 = OK
        if (!res.ok) throw new Error("Error en la peticion " + res.status);
        return await res.json();
    } catch (error) {
        console.log(error);
        alert("Ocurrió un error");
        return null;
    }
}

// Convertir imagen a base64
function toBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        // Obtenemos el archivo
        reader.onload = () => resolve(reader.result.split(",")[1]);

        // Si hubo un error, se devuelve aquí
        reader.onerror = reject;
    });
}

//Listar todos los Juegos
async function loadGames(params = {}) {
    const query = new URLSearchParams(params).toString();

    // Viene en forma de promesa
    const games = await fetchJson(`${API_URL}?${query}`) //Viene en formato JSON
    if (!games) return;

    //Obteniendo el tbody del html
    const tbody = document.querySelector("#games-table tbody");
    tbody.innerHTML = "";

    games.forEach(m => tbody.appendChild(createGameRow(m)));
}

function createGameRow(m) {
    const row = document.createElement("tr");
    row.innerHTML = `
        <td>${m.id}</td>
        <td>${m.titulo}</td>
        <td>${m.desarrolladora}</td>
        <td>${m.anio}</td>
        <td>${m.genero}</td>
        <td>${m.rating}</td>
        <td>
            <img width='100' 
                src='data:image/png;base64,${m.imagen}' />
        </td>
        <td>
            <button onclick="editGame(${m.id})"
                class='button m-2 is-warning'>Editar</button>
            <button onclick="deleteGame(${m.id})"
                class='button m-2 is-danger'>Eliminar</button>
        </td>
    `;
    return row;
}

document.addEventListener("click", e => {
    const btn = e.target.closest("button[data-action]");
    if (!btn) return;

    const id = btn.dataset.id;
    const action = btn.dataset.action;
    if (action === "edit") return editGame(id);
    if (action === "delete") return deleteGame(id);
});

// Eliminar Juegos

async function deleteGame(id) {
    if (!confirm("¿Estás seguro de que deseas eliminar este juego?")) return;

    const data = await fetchJson(API_URL + id, { method: "DELETE" });
    if (data) {
        alert(data.message);
        loadGames();
    }
}

// Editar Juegos

function editGame(id) {
    window.location.href = `form.html?id=` + id;
}

async function initform() {
    const form = document.getElementById("game-form");
    // Obtener parametro que viene de la URL
    const params = new URLSearchParams(window.location.search);
    const gameid = params.get("id");

    const imagen_actual_input = document.getElementById("imagen_actual");
    const imagen_preview = document.getElementById("imagen-preview");
    const preview_field = document.getElementById("preview-field");
    const file_name = document.getElementById("file-name");
    const fileinput = document.getElementById("imagen");

    setupFileInput(fileinput, file_name, imagen_preview, preview_field);

    if (gameid) {
        await loadGameData(gameid, form, file_name, imagen_preview, preview_field, imagen_actual_input);
    }

    form.addEventListener("submit", async (e) => {
        handleForSubmit(e, form, fileinput, imagen_actual_input, gameid);
    });

}

async function loadGameData(id, form, fileNameSpan, imagenPreview, previewField, imagenActualInput) {
    document.getElementById("form-title").textContent = "Editar VideoJuego";
    document.getElementById("game-id").value = id;

    const game = await fetchJson(API_URL + id);
    if (!game) return;

    const fields = ["titulo", "desarrolladora", "anio", "genero", "rating"];
    fields.forEach(f => form[f].value = game[f]);

    if (game.imagen) {
        imagenActualInput.value = game.imagen;
        imagenPreview.src = `data:image/png;base64,${game.imagen}`;
        previewField.style.display = ""; // Muestra la imagen
        fileNameSpan.textContent = "Imagen Actual Cargada";
    }

    /*
    form.titulo.value = game.titulo;
    form.desarrolladora.value = game.desarrolladora;
    form.anio.value = game.anio;
    form.genero.value = game.genero;
    form.rating.value = game.rating;    
    */
}

function setupFileInput(fileInput, fileNameSpan, imagenPreview, previewField) {
    if (!fileInput) return;

    fileInput.addEventListener("change", () => {
        if (fileInput.files.length > 0) {
            const file = fileinput.files[0];
            fileNameSpan.textContent = file.name;
            imagenPreview.src = URL.createObjectURL(file);
            previewField.style.display = ""; // Muestra la imagen
        } else {
            fileNameSpan.textContent = "Ningun Archivo Seleccionado";
            previewField.style.display = "none"; // Oculta la imagen
        }
    });
}

async function handleForSubmit(e, form, fileInput, imagen_actual_input, gameid) {
    e.preventDefault();

    const formData = new FormData(form);
    const game = Object.fromEntries(formData);

    if(fileInput.files.length > 0) {
        game.imagen = await toBase64(fileInput.files[0]);
    }else{
        game.imagen = imagen_actual_input.value || "";
    }

    let url = API_URL;
    let method = "POST";

    if (gameid) {
        method = "PUT";
        url = API_URL + gameid;
    }

    const data = await fetchJson(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(game),
    });

    if (data) {
        alert(data.message);
        window.location.href = "index.html";
    }

}

function getFilters() {
    return {
        genero: document.querySelector('#filter-genero').value.trim(),
        min_rating: document.querySelector('#filter-rating').value.trim()
    }
}

document.addEventListener('DOMContentLoaded', () => {
    loadGames();

    const filterBtn = document.querySelector('#filter-btn');

    filterBtn.addEventListener('click', () => {
        const filters = getFilters();
        loadGames(filters);
    });
});


