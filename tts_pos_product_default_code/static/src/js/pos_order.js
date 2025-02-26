import { PosOrder } from "@point_of_sale/app/models/pos_order";
import { omit } from "@web/core/utils/objects";
import { patch } from "@web/core/utils/patch";

patch(PosOrder.prototype, {
    //@override
    export_for_printing(baseUrl, headerData) {
        var res = super.export_for_printing(...arguments);

        res.orderlines = this.getSortedOrderlines().map((l) =>
                omit(l.getDisplayData(true), "internalNote"));

        return res;
    }
});