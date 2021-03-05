
const searchProd = document.querySelector("#searchProd");
const tableOutput = document.querySelector(".table-output");
const appTable = document.querySelector(".app-table");
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
                        <td><button onclick="det(${item.id})" class='btn btn-primary btn-sm my-1'>Detalle</button></td>
                        <td><button data-product=${item.id} data-action='add' href='' class='btn btn-success btn-sm my-1 update-cart'>Al Canasto</button></td>
                    `
                });
            }
        });
    }else{
        appTable.style.display = "block";
        tableOutput.style.display = "none";
    }
})


function det(id){
    console.log(id)
    location.href="/prod_detail/${id}'"

}


