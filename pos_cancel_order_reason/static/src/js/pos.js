import { Component } from "@odoo/owl";
import { Orderline } from "@point_of_sale/app/generic_components/orderline/orderline";
import { OrderWidget } from "@point_of_sale/app/generic_components/order_widget/order_widget";
import { ReceiptHeader } from "@point_of_sale/app/screens/receipt_screen/receipt/receipt_header/receipt_header";
import { omit } from "@web/core/utils/objects";
import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/store/pos_store";
import { ReceiptScreen } from "@point_of_sale/app/screens/receipt_screen/receipt_screen";
import {
    makeAwaitable,
    ask,
    makeActionAwaitable,
} from "@point_of_sale/app/store/make_awaitable_dialog";
import { SelectionPopup } from "@point_of_sale/app/utils/input_popups/selection_popup";
import { _t } from "@web/core/l10n/translation";


patch(PosStore.prototype, {
        async onDeleteOrder(order) {
        if (order.get_orderlines().length > 0) {
        const ReasonList = [];
        for (const reason of this.models["pos.order.cancel.reason"].getAll()) {
            ReasonList.push({
                id: reason.id,
                label: reason.name,
                item: reason,
            });
        }
          const selectedReason = await makeAwaitable(this.dialog, SelectionPopup, {
            list: ReasonList,
            title: _t("Please Choose the Reason"),
        });
        if (selectedReason){
         if (selectedReason === "none") {
            this.get_order().update({
                reason_id: false,
            });
            return;
        }

        this.get_order().update({
            reason_id: selectedReason ? selectedReason.id : false,
        });
                    const confirmed = await ask(this.dialog, {
                title: _t("Existing orderlines"),
                body: _t(
                    "%s has a total amount of %s, are you sure you want to delete this order?",
                    order.pos_reference,
                    this.env.utils.formatCurrency(order.get_total_with_tax())
                ),
            });
            if (!confirmed) {
                return false;
            }
        }

        }
        const orderIsDeleted = await this.deleteOrders([order]);
        if (orderIsDeleted) {
            order.uiState.displayed = false;
            this.afterOrderDeletion();
        }
        return orderIsDeleted;
    },
});
