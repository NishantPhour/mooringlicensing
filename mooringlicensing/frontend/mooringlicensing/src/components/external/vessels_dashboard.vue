<template>
    <div class="container" id="externalDash">
        <FormSection :formCollapse="false" label="Vessels" Index="vessels">
            <div class="row">
                <div class="col-sm-10">
                </div>
            </div>

            <datatable 
                ref="vessels_datatable" 
                id="vessels_datatable" 
                :dtOptions="datatable_options" 
                :dtHeaders="datatable_headers"
            />
            <div v-if="recordSaleId">
                <RecordSale 
                ref="record_sale" 
                :recordSaleId="recordSaleId"
                :key="recordSaleKey"
                @closeModal="closeModal"
                @refreshDatatable="refreshFromResponse"
                />
            </div>
        </FormSection>
    </div>
</template>

<script>
import datatable from '@/utils/vue/datatable.vue'
import FormSection from "@/components/forms/section_toggle.vue"
import { api_endpoints, helpers } from '@/utils/hooks'
import RecordSale from './record_sale.vue'

export default {
    name: 'VesselsDashboard',
    data() {
        let vm = this;
        return {
            recordSaleId: null,
            uuid: 0,
            // Datatable settings
            datatable_headers: ['Name', 'Registration', 'Length', 'Draft', 'Type', 'Owner', 'Sale date', 'Action'],
            datatable_options: {
                autoWidth: false,
                language: {
                    processing: "<i class='fa fa-4x fa-spinner fa-spin'></i>"
                },
                responsive: true,
                searching: true,
                ajax: {
                    "url": api_endpoints.vessel_external_list + '?format=datatables',
                    "dataSrc": 'data',
                },
                dom: 'lBfrtip',
                buttons:[],
                columns: [
                    {
                        data: "vessel_details.vessel_name",
                        orderable: false,
                        searchable: false,
                        visible: true,
                    },
                    {
                        data: "vessel_details.rego_no",
                        orderable: true,
                        searchable: true,
                        visible: true,
                    },
                    {
                        data: "vessel_details.vessel_length",
                        orderable: true,
                        searchable: true,
                        visible: true,
                    },
                    {
                        data: "vessel_details.vessel_draft",
                        orderable: true,
                        searchable: true,
                        visible: true,
                    },
                    {
                        data: "vessel_details.vessel_type",
                        orderable: true,
                        searchable: true,
                        visible: true,
                    },
                    {
                        data: "owner_name",
                        orderable: true,
                        searchable: true,
                        visible: true,
                    },
                    {
                        data: "sale_date",
                        orderable: true,
                        searchable: true,
                        visible: true,
                    },
                    {
                        data: "id",
                        orderable: true,
                        searchable: true,
                        visible: true,
                        'render': function(row, type, full){
                            let links = '';
                            if (!full.sale_date) {
                                links += `<a href='/external/vesselownership/${full.id}'>View</a><br/>`;
                                links += full.record_sale_link;
                            }
                            return links
                        }
                    },
                ],
                processing: true,
            },
        }
    },
    components:{
        FormSection,
        datatable,
        RecordSale,
    },
    watch: {
    },
    computed: {
        recordSaleKey: function() {
            return `${this.recordSaleId}_${this.uuid}`
        },
    },
    methods: {
        closeModal: function() {
            this.uuid++;
        },
        addVessel: function() {
            this.$router.push({
                name: 'new-vessel'
            });
        },
        refreshFromResponse: async function(){
            await this.$refs.vessels_datatable.vmDataTable.ajax.reload();
        },
        openSaleModal: function() {
            this.$nextTick(() => {
                console.log(this.recordSaleId)
                this.$refs.record_sale.isModalOpen = true;
            });
        },
        addEventListeners: function() {
            let vm = this;
            let table = vm.$refs.vessels_datatable.vmDataTable

            table.on('click', 'a[data-id]', async function(e) {
                e.preventDefault();
                var id = $(this).attr('data-id');
                vm.recordSaleId = parseInt(id);
                vm.openSaleModal();
            });
        }
    },
    mounted: function () {
        this.$nextTick(() => {
            this.addEventListeners();
        });

    },
}
</script>
<style lang="css" scoped>
    button {
        width: 100%;
        height: 100%;
    }
</style>
