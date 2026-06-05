const form = document.getElementById('searchForm');
const resultsDiv = document.getElementById('results');
const comparisonDiv = document.getElementById('comparison');
const comparisonTableBody = document.querySelector('#comparisonTable tbody');
let selectedProducts = [];

// Search form submit
form.addEventListener('submit', function(e){
    e.preventDefault();
    const query = document.getElementById('query').value;
    const category = document.getElementById('category').value;
    const budget = document.getElementById('budget').value;
    const preference = document.getElementById('preference').value;

    fetch(`/api/products?query=${query}&category=${category}&budget=${budget}&preference=${preference}`)
    .then(res => res.json())
    .then(products => {
        displayResults(products);
    });
});

// Display search results
function displayResults(products){
    resultsDiv.innerHTML = '';
    selectedProducts = [];
    if(products.length===0){ resultsDiv.innerHTML='<p>❌ No products found.</p>'; return; }

    products.forEach((p,index) => {
        const card = document.createElement('div');
        card.className = 'card';
        card.innerHTML = `
            <h3>${p.name}</h3>
            <p>Category: ${p.category}</p>
            <p>Price: $${p.price}</p>
            <p>Rating: ${p.rating} | Reviews: ${p.reviews}</p>
            <p>Source: ${p.source}</p>
            <button onclick="addToCompare(${index})">Compare</button>
        `;
        resultsDiv.appendChild(card);
    });
}

// Compare products (up to 3)
function addToCompare(idx){
    if(selectedProducts.length>=3){ alert('Max 3 products'); return; }
    selectedProducts.push(idx);
    updateComparison();
}

function updateComparison(){
    comparisonTableBody.innerHTML = '';
    comparisonDiv.style.display = 'block';
    selectedProducts.forEach(idx=>{
        const card = document.querySelectorAll('.card')[idx];
        const name = card.querySelector('h3').innerText;
        const category = card.querySelector('p:nth-child(2)').innerText.split(': ')[1];
        const price = card.querySelector('p:nth-child(3)').innerText.split('$')[1];
        const rating = card.querySelector('p:nth-child(4)').innerText.split('|')[0].split(': ')[1];
        const reviews = card.querySelector('p:nth-child(4)').innerText.split('|')[1].split(': ')[1];
        const source = card.querySelector('p:nth-child(5)').innerText.split(': ')[1];
        const row = document.createElement('tr');
        row.innerHTML = `<td>${name}</td><td>${category}</td><td>${price}</td><td>${rating}</td><td>${reviews}</td><td>${source}</td>`;
        comparisonTableBody.appendChild(row);
    });
}

// Budget Planner
function planBudget(){
    const totalBudget = parseFloat(document.getElementById('totalBudget').value);
    if(!totalBudget){ alert('Enter a budget'); return; }

    fetch(`/api/products`)
    .then(res => res.json())
    .then(allProducts => {
        let filtered = allProducts.filter(p => p.price <= totalBudget);
        filtered.sort((a,b)=>(b.rating + b.reviews/1000) - (a.rating + a.reviews/1000));
        displayBudgetResults(filtered,totalBudget);
    });
}

function displayBudgetResults(products,totalBudget){
    const container = document.getElementById('budgetResults');
    container.innerHTML = `<p>Products under $${totalBudget}:</p>`;
    if(products.length===0){ container.innerHTML+=`<p>❌ No products fit your budget.</p>`; return; }
    const list = document.createElement('ul');
    products.forEach(p=>{
        const li = document.createElement('li');
        li.innerText = `${p.name} - $${p.price} | Rating: ${p.rating} | Reviews: ${p.reviews}`;
        list.appendChild(li);
    });
    container.appendChild(list);
}

// Top-N Recommendations
function showTopN(){
    const N = 5;
    fetch(`/api/products`)
    .then(res => res.json())
    .then(allProducts => {
        allProducts.sort((a,b)=>(b.rating + b.reviews/1000) - (a.rating + a.reviews/1000));
        displayTopN(allProducts.slice(0,N));
    });
}

function displayTopN(products){
    const container = document.getElementById('topResults');
    container.innerHTML = '';
    products.forEach(p=>{
        const div = document.createElement('div');
        div.innerText = `${p.name} - $${p.price} | Rating: ${p.rating} | Reviews: ${p.reviews}`;
        container.appendChild(div);
    });
}