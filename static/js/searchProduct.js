
const searchProd = document.querySelector("#searchProd");
const appTable = document.querySelector(".app-table");
const tableOutput = document.querySelector(".table-output");
const tbody = document.querySelector(".table-search");
tableOutput.style.display='none';

searchProd.addEventListener('keyup', (e) => {
    const searchValue = e.target.value;

    if(searchValue.trim().length > 0){
        console.log("searchValue :", searchValue)

        fetch(".", {
            body: JSON.stringify({ searchText: searchValue}), method: "POST",
        })
        .then((res) => res.json())
        .then((data) => {
            console.log("data", data);
            appTable.style.display = "none";
            tableOutput.style.display = "block";

            if(data.length === 0){
                tableOutput.innerHTML = "No se encontraron resultados"
            }else{
                data.forEach((item) => {
                    tbody.innerHTML += `
                        <td>${item.name}</td>
                        <td>${item.presenta}</td>
                        <td>${item.price}</td>
                        <td>${item.discount_price}</td>
                        <td>${item.label}</td>
                    `
                });
            }
        });
    }else{
        appTable.style.display = "block";
        tableOutput.style.display = "none";
    }
})
