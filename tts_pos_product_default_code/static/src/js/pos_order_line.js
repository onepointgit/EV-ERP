import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";
import { patch } from "@web/core/utils/patch";

patch(PosOrderline.prototype, {
    getDisplayData(export_for_printing=false) {
        var product_default_code = '';

        if(!export_for_printing || this.config.print_product_default_code_receipt){
            product_default_code = this.get_product_default_code();
        }
        
        return {
            ...super.getDisplayData(),
            product_default_code: product_default_code,
        };
    },
    get_product_default_code() {
        return this.get_product().get_default_code();
    }
});