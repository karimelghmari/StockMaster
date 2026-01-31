// --- LOGIN ---
async function handleLogin() {
    localStorage.clear(); 
    const username = document.getElementById('usernameInput').value;
    const password = document.getElementById('passwordInput').value;
    const errorDiv = document.getElementById('errorMessage');

    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    try {
        const response = await fetch('/auth/login', {
            method: 'POST',
            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
            body: formData
        });
        const data = await response.json();
        if (response.ok) {
            localStorage.setItem('token', data.access_token);
            window.location.href = "/dashboard";
        } else {
            errorDiv.innerText = data.detail || "Login failed";
            errorDiv.style.display = "block";
        }
    } catch (error) {
        errorDiv.innerText = "Cannot connect to server";
        errorDiv.style.display = "block";
    }
}

// --- LOGOUT ---
function logout() {
    localStorage.clear();
    window.location.href = "/login";
}

// --- CHARGER LES PRODUITS ET STATS ---
async function loadProducts() {
    const token = localStorage.getItem('token');
    if (!token) return;

    const response = await fetch('/products/', {
        headers: { 'Authorization': `Bearer ${token}` }
    });

    if (response.ok) {
        const products = await response.json();
        const tableBody = document.getElementById('product-table-body');
        tableBody.innerHTML = ''; 

        // Mise à jour des Stats
        const totalValue = products.reduce((sum, p) => sum + (p.price * p.quantity), 0);
        const lowStockCount = products.filter(p => p.quantity <= 5).length;
        
        if(document.getElementById('stat-total-products')) {
            document.getElementById('stat-total-products').innerText = products.length;
            document.getElementById('stat-total-value').innerText = totalValue.toFixed(2) + " €";
            document.getElementById('stat-low-stock').innerText = lowStockCount;
        }

        products.forEach(p => {
            const rowClass = p.quantity <= 5 ? 'stock-low' : '';
            tableBody.innerHTML += `
                <tr class="${rowClass}">
                    <td>${p.id}</td>
                    <td><strong>${p.name}</strong></td>
                    <td>${p.description || '-'}</td>
                    <td>${p.price.toFixed(2)} €</td>
                    <td><span class="badge ${p.quantity <= 5 ? 'bg-danger' : 'bg-dark'}">${p.quantity}</span></td>
                    <td>
                        <div class="btn-group me-2">
                            <button onclick="makeQuickTransaction(${p.id}, 'sale')" class="btn btn-sm btn-danger">Vendre</button>
                            <button onclick="makeQuickTransaction(${p.id}, 'restock')" class="btn btn-sm btn-success">+ Stock</button>
                        </div>
                        <button onclick="editProduct(${p.id}, '${p.name}', ${p.price}, ${p.quantity})" class="btn btn-sm btn-warning"><i class="bi bi-pencil"></i></button>
                        <button onclick="deleteProduct(${p.id})" class="btn btn-sm btn-outline-danger ms-1"><i class="bi bi-trash"></i></button>
                    </td>
                </tr>
            `;
        });
    }
}

// --- TRANSACTIONS (VENDRE / REAPPRO) ---
async function makeQuickTransaction(productId, type) {
    const qty = prompt(`Quantité pour la ${type === 'sale' ? 'vente' : 'réception'} :`, "1");
    if (qty === null || isNaN(qty) || qty <= 0) return;

    const token = localStorage.getItem('token');
    try {
        const response = await fetch('/transactions/', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                product_id: productId,
                quantity: parseInt(qty),
                type: type
            })
        });

        if (response.ok) {
            loadProducts();      // Rafraîchit le stock et stats
            loadTransactions();  // Rafraîchit l'historique
        } else {
            const errorData = await response.json();
            alert("Erreur : " + (errorData.detail || "Action impossible"));
        }
    } catch (err) {
        console.error("Erreur réseau :", err);
    }
}

// --- HISTORIQUE ---
async function loadTransactions() {
    const token = localStorage.getItem('token');
    if (!token) return;
    try {
        const response = await fetch('/transactions/', {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (response.ok) {
            const txs = await response.json();
            const txBody = document.getElementById('transaction-history-body');
            if(!txBody) return;
            txBody.innerHTML = '';

            txs.reverse().slice(0, 10).forEach(t => {
                const badge = t.type === 'sale' ? '<span class="badge-sale">VENTE</span>' : '<span class="badge-restock">ACHAT</span>';
                const date = new Date(t.date).toLocaleString('fr-FR');
                txBody.innerHTML += `
                    <tr>
                        <td>${date}</td>
                        <td>#${t.product_id}</td>
                        <td>${badge}</td>
                        <td><strong>${t.quantity}</strong></td>
                    </tr>
                `;
            });
        }
    } catch (err) { console.error(err); }
}

// --- AJOUTER PRODUIT ---
document.getElementById('addProductForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const token = localStorage.getItem('token');
    const productData = {
        name: document.getElementById('newName').value,
        description: document.getElementById('newDesc').value,
        price: parseFloat(document.getElementById('newPrice').value),
        quantity: parseInt(document.getElementById('newQty').value),
        min_stock_level: 5
    };

    const response = await fetch('/products/', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
        body: JSON.stringify(productData)
    });

    if (response.ok) {
        document.getElementById('addProductForm').reset();
        loadProducts();
    }
});

// --- SUPPRIMER ---
async function deleteProduct(productId) {
    if (!confirm("Supprimer ce produit ?")) return;
    const token = localStorage.getItem('token');
    const response = await fetch(`/products/${productId}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
    });
    if (response.ok) loadProducts();
}

// --- MODIFIER ---
async function editProduct(id, name, currentPrice, currentQty) {
    const newPrice = prompt(`Nouveau prix pour ${name}:`, currentPrice);
    const newQty = prompt(`Nouvelle quantité pour ${name}:`, currentQty);
    if (newPrice === null || newQty === null) return;

    const token = localStorage.getItem('token');
    await fetch(`/products/${id}`, {
        method: 'PUT',
        headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({ price: parseFloat(newPrice), quantity: parseInt(newQty) })
    });
    loadProducts();
}

function logout() {
    localStorage.clear();
    sessionStorage.clear();
    window.location.href = "/login";
}