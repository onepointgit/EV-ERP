import { Component } from "@odoo/owl";
import { Orderline } from "@point_of_sale/app/generic_components/orderline/orderline";
import { OrderWidget } from "@point_of_sale/app/generic_components/order_widget/order_widget";
import { ReceiptHeader } from "@point_of_sale/app/screens/receipt_screen/receipt/receipt_header/receipt_header";
import { omit } from "@web/core/utils/objects";
import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/store/pos_store";
import { ReceiptScreen } from "@point_of_sale/app/screens/receipt_screen/receipt_screen";

export class OrderReceipt2 extends Component {
    static template = "point_of_sale.OrderReceipt2";
    static components = {
        Orderline,
        OrderWidget,
        ReceiptHeader,
    };
    static props = {
        data: Object,
        formatCurrency: Function,
        basic_receipt: { type: Boolean, optional: true },
    };
    static defaultProps = {
        basic_receipt: false,
    };
    omit(...args) {
        return omit(...args);
    }
    doesAnyOrderlineHaveTaxLabel() {
        return this.props.data.orderlines.some((line) => line.taxGroupLabels);
    }
    getPortalURL() {
        return `${this.props.data.base_url}/pos/ticket`;
    }
}


patch(PosStore.prototype, {
    async processServerData() {
        await super.processServerData(...arguments);
        var test = []
        for(var i=0;i<this.config.multi_receipt_count;i++){
            test.push(i);
        }
        this.env.test = test;
        console.log("Testing test>>>>>>>>>>>>>>>>>",this.config.multi_receipt_count);

    },
});

patch(ReceiptScreen.prototype, {
    async generateTicketImage(isBasicReceipt = false) {
        return await this.renderer.toJpeg(
            OrderReceipt2,
            {
                data: this.pos.orderExportForPrinting(this.pos.get_order()),
                formatCurrency: this.env.utils.formatCurrency,
                basic_receipt: isBasicReceipt,
            },
            { addClass: "pos-receipt-print p-3" }
        );
    },
});


// odoo.define('pos_multi_receipt.pos_multi_receipt', function(require){
//
//     var models = require('point_of_sale.models');
//
//     var PosModelSuper = models.PosModel;
//     models.PosModel = models.PosModel.extend({
//         after_load_server_data: function(){
//             var res = PosModelSuper.prototype.after_load_server_data.call(this);
//             this.test = _.range(this.config.multi_receipt_count);
//             return res;
//         },
//     });
// });
