import { CategorySelector } from "@point_of_sale/app/generic_components/category_selector/category_selector";
import { patch } from "@web/core/utils/patch";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
var flag = false;

import { onMounted } from "@odoo/owl";

patch(CategorySelector.prototype, {
	onClickList(){
        let prod_list_cont = document.getElementById("product-list")
        prod_list_cont.classList.remove('d-none')
        let prod_grid_cont = document.getElementsByClassName("product-list")
        prod_grid_cont[1].classList.add('d-none')

	},

    onClickGrid(){
        let prod_list_cont = document.getElementById("product-list")
        prod_list_cont.classList.add('d-none')
        let prod_grid_cont = document.getElementsByClassName("product-list")
        prod_grid_cont[1].classList.remove('d-none')
    }
});

patch(ProductScreen.prototype, {
	setup() {
        super.setup();
        onMounted(this.onMounted);
    },

    get productsToDisplay() {
        // const { db } = this.pos;
        // let prods = super.productsToDisplay;
        let list = [];
        this.Changeview()
        if (this.searchWord !== "") {
            list = this.addMainProductsToDisplay(this.getProductsBySearchWord(this.searchWord));
            return list;
        } else {
            var AscName, DescName, LowToHighPrice, HighToLowPrice;
            var product = super.productsToDisplay;
            if(flag == true){
                document.querySelectorAll('.product-list').forEach(function(element) {
                    element.style.display = 'none';
                });
            }
            if(this.pos.config.product_ordering == "a_to_z") {
                function SortByNameAsc(firstName, secondName){
                    var firstName = firstName.name.toLowerCase();
                    var secondName = secondName.name.toLowerCase();
                    var final_name_asc = ((firstName < secondName) ? -1 : ((firstName > secondName) ? 1 : 0));
                    return final_name_asc
                }
                AscName = product.sort(SortByNameAsc);
                return AscName;
            } else if (this.pos.config.product_ordering == "z_to_a"){
                function SortByNameDesc(firstName, secondName){
                    var firstName = firstName.name.toLowerCase();
                    var secondName = secondName.name.toLowerCase();
                    var final_name_desc = ((firstName > secondName) ? -1 : ((firstName < secondName) ? 1 : 0));
                    return final_name_desc;
                }
                DescName = product.sort(SortByNameDesc);
                return DescName;
            } else if (this.pos.config.product_ordering == "low_to_high"){
                function SortByPriceLowToHigh(firstPrice, secondPrice){
                    var firstPrice = firstPrice.lst_price;
                    var secondPrice = secondPrice.lst_price;
                    var final_price_low_to_high = parseFloat(firstPrice) - parseFloat(secondPrice);
                    return final_price_low_to_high
                }
                LowToHighPrice = product.sort(SortByPriceLowToHigh);
                return LowToHighPrice;
            } else if (this.pos.config.product_ordering == "high_to_low") {
                function SortByPriceHighToLow(firstPrice, secondPrice){
                    var firstPrice = firstPrice.lst_price;
                    var secondPrice = secondPrice.lst_price;
                    var final_price_high_to_low = parseFloat(secondPrice) - parseFloat(firstPrice);
                    return final_price_high_to_low
                }
                HighToLowPrice = product.sort(SortByPriceHighToLow);
                return HighToLowPrice;
            } else {
                return product;
            }
        }
    },

    get imageUrl() {
        const product = this.prd.id
         return `/web/image?model=product.product&field=image_128&id=${product}&unique=${product.write_date}`;
    },
    get pricelist() {
        const current_order = this.env.services.pos.get_order();
        if (current_order) {
            return current_order.pricelist;
        }
        return this.env.services.pos.default_pricelist;
    },
    get price() {
        const product = this.prd
        const formattedUnitPrice = this.env.utils.formatCurrency(this.pos.getProductPrice(product));
        if (product.to_weight) {
            return `${formattedUnitPrice}/${product.uom_id.name}`;
        } else {
            return formattedUnitPrice;
        }

    },

    onClickHeader(){
        this.Changeview()
    },

    Changeview(){
        var self = this;

        document.addEventListener("click", (event) => {
            
            if (event.target.className == 'code'){
                var table, i, x, y,dir,switchcount=0;;
                table = document.getElementById("id01");
                var switching = true;
                dir = "asc";
                while (switching){
                    switching = false;
                    var rows = table.rows;
                    for (i = 1; i < (rows.length - 1); i++){
                        var Switch = false;
                        x = rows[i].getElementsByClassName("product_code")[0];
                        y = rows[i + 1].getElementsByClassName("product_code")[0];
                        if(dir== "asc"){
                            if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()){

                                Switch = true;
                                break;
                            }
                        }
                        else if (dir == "desc") {
                            if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                                Switch = true;
                                break;
                            }
                        }
                    }
                    if (Switch) {
                        rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
                        switching = true;
                        switchcount ++;
                    } else {
                        if (switchcount == 0 && dir == "asc") {
                            dir = "desc";
                            switching = true;
                        }
                    }
                }
            }

            if (event.target.className == 'name'){
                var table, i, x, y,dir,switchcount=0;;
                table = document.getElementById("id01");
                var switching = true;
                dir = "asc";
                while (switching){
                    switching = false;
                    var rows = table.rows;
                    for (i = 1; i < (rows.length - 1); i++){
                        var Switch = false;
                        x = rows[i].getElementsByClassName("product_name")[0];
                        y = rows[i + 1].getElementsByClassName("product_name")[0];
                        if(dir== "asc"){
                            if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()){
                                Switch = true;
                                break;
                            }
                        }
                        else if (dir == "desc") {
                            if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                                Switch = true;
                                break;
                            }
                        }
                    }
                    if (Switch) {
                        rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
                        switching = true;
                        switchcount ++;
                    } else {
                        if (switchcount == 0 && dir == "asc") {
                            dir = "desc";
                            switching = true;
                        }
                    }
                }
            }

            if (event.target.className == 'type'){
                var table, i, x, y,dir,switchcount=0;;
                table = document.getElementById("id01");
                var switching = true;
                dir = "asc";
                while (switching){
                    switching = false;
                    var rows = table.rows;
                    for (i = 1; i < (rows.length - 1); i++){
                        var Switch = false;
                        x = rows[i].getElementsByClassName("product_type")[0];
                        y = rows[i + 1].getElementsByClassName("product_type")[0];
                        if(dir== "asc"){
                            if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()){
                                Switch = true;
                                break;
                            }
                        }
                        else if (dir == "desc") {
                            if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                                Switch = true;
                                break;
                            }
                        }
                    }
                    if (Switch) {
                        rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
                        switching = true;
                        switchcount ++;
                    } else {
                        if (switchcount == 0 && dir == "asc") {
                            dir = "desc";
                            switching = true;
                        }
                    }
                }
            }

            if (event.target.className == 'uom'){
                var table, i, x, y,dir,switchcount=0;;
                table = document.getElementById("id01");
                var switching = true;
                dir = "asc";
                while (switching){
                    switching = false;
                    var rows = table.rows;
                    for (i = 1; i < (rows.length - 1); i++){
                        var Switch = false;
                        x = rows[i].getElementsByClassName("product_uom")[0];
                        y = rows[i + 1].getElementsByClassName("product_uom")[0];
                        if(dir== "asc"){
                            if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()){
                                Switch = true;
                                break;
                            }
                        }
                        else if (dir == "desc") {
                            if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {

                                Switch = true;
                                break;
                            }
                        }
                    }
                    if (Switch) {
                        rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
                        switching = true;
                        switchcount ++;
                    } else {
                        if (switchcount == 0 && dir == "asc") {
                            dir = "desc";
                            switching = true;
                        }
                    }
                }
            }

            if (event.target.className == 'price'){

                var table, i, x, y,z,dir,switchcount=0;
                table = document.getElementById("id01");
                var switching = true;
                dir = "asc";
                while (switching){
                    switching = false;
                    var rows = table.rows;
                    for (i = 1; i < (rows.length - 1); i++){
                        var Switch = false;
                        x = rows[i].getElementsByClassName("product_price")[0];
                        y = rows[i + 1].getElementsByClassName("product_price")[0];
                        z = x.innerHTML.split(";")[1].split(",").join("")
                        if(dir== "asc"){
                            if (parseFloat(x.innerHTML.split(";")[1].split(",").join("")) > parseFloat(y.innerHTML.split(";")[1].split(",").join(""))){
                                Switch = true;
                                break;
                            }
                        }
                        else if (dir == "desc") {
                            if (parseFloat(x.innerHTML.split(";")[1].split(",").join("")) < parseFloat(y.innerHTML.split(";")[1].split(",").join(""))) {
                                Switch = true;
                                break;
                            }
                        }
                    }
                    if (Switch) {
                        rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
                        switching = true;
                        switchcount ++;
                    } else {
                        if (switchcount == 0 && dir == "asc") {
                            dir = "desc";
                            switching = true;
                        }
                    }
                }

            }
            if (event.target.className == 'qty'){
                var table, i, x, y ,dir,switchcount=0;
                table = document.getElementById("id01");
                var switching = true;
                dir = "asc";
                while (switching){
                    switching = false;
                    var rows = table.rows;
                    for (i = 1; i < (rows.length - 1); i++){
                        var Switch = false;
                        x = rows[i].getElementsByClassName("on_hand_qty")[0];
                        y = rows[i + 1].getElementsByClassName("on_hand_qty")[0];
                        if(dir== "asc"){
                            if (parseInt(x.innerHTML) > parseInt(y.innerHTML)){

                                Switch = true;
                                break;
                            }
                        }
                        else if (dir == "desc") {
                            if (parseInt(x.innerHTML) < parseInt(y.innerHTML)) {

                                Switch = true;
                                break;
                            }
                        }
                    }
                    if (Switch) {
                        rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
                        switching = true;
                        switchcount ++;
                    } else {
                        if (switchcount == 0 && dir == "asc") {
                            dir = "desc";
                            switching = true;
                        }
                    }
                }
            }
            if (event.target.className == 'fqty'){
                var table, i, x, y ,dir,switchcount=0;
                table = document.getElementById("id01");
                var switching = true;
                dir = "asc";
                while (switching){
                    switching = false;
                    var rows = table.rows;
                    for (i = 1; i < (rows.length - 1); i++){
                        var Switch = false;
                        x = rows[i].getElementsByClassName("forecast_qty")[0];
                        y = rows[i + 1].getElementsByClassName("forecast_qty")[0];
                        if(dir== "asc"){
                            if (parseInt(x.innerHTML) > parseInt(y.innerHTML)){

                                Switch = true;
                                break;
                            }
                        }
                        else if (dir == "desc") {
                            if (parseInt(x.innerHTML) < parseInt(y.innerHTML)) {

                                Switch = true;
                                break;
                            }
                        }
                    }
                    if (Switch) {
                        rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
                        switching = true;
                        switchcount ++;
                    } else {
                        if (switchcount == 0 && dir == "asc") {
                            dir = "desc";
                            switching = true;
                        }
                    }
                }
            };
        })

           
    },

    onMounted() {
        if(this.pos.config.prod_view === 'list' && this.pos.config.enable_list_view){

            let prod_list_cont = document.getElementById("product-list")
            prod_list_cont.classList.remove('d-none')
            let prod_grid_cont = document.getElementsByClassName("product-list")
            prod_grid_cont[1].classList.add('d-none')

        	
        }
        else if (this.pos.config.prod_view === 'grid' && this.pos.config.enable_list_view){

            let prod_list_cont = document.getElementById("product-list")
            prod_list_cont.classList.add('d-none')
            let prod_grid_cont = document.getElementsByClassName("product-list")
            prod_grid_cont[1].classList.remove('d-none')
        }
    },
});