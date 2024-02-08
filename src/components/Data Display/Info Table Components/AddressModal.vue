<template>
    <div>
        <TransitionRoot :show="isAddressModalOpen" as="template">
            <Dialog as="div" class="fixed inset-0 overflow-y-auto z-50">
                <div class="flex min-h-full items-center justify-center p-4 text-center">
                    <div class="fixed inset-0 bg-black bg-opacity-50" aria-hidden="true"></div>
                    <TransitionChild
                        as="template"
                        enter="duration-300 ease-out"
                        enter-from="opacity-0 scale-95"
                        enter-to="opacity-100 scale-100"
                        leave="duration-200 ease-in"
                        leave-from="opacity-100 scale-100"
                        leave-to="opacity-0 scale-95"
                    >
                        <DialogPanel class="w-full md:w-[800px] transform overflow-hiddenformErrMsg rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all dark:bg-gray-800 z-50">
                            <button @click="closeAddressModal" class="absolute top-4 left-4 bg-transparent text-black hover:text-gray-700 font-semibold text-xl leading-none transition-transform transform hover:scale-110">
                                <XMarkIcon class="w-6 h-6 dark:text-gray-200" />
                            </button>
                            <DialogTitle as="h3" class="text-lg text-center font-medium leading-6 text-gray-900 dark:text-gray-200">
                                {{ modalTitle }}
                            </DialogTitle>
                            <AddressLookup></AddressLookup>
                            <div class="text-center mt-4">
                                <p v-if="formErrMsg" class="text-sm text-red-600 mt-1 mb-2">{{ formErrMsg }}</p>
                                <button @click="handleAddressAction" class="rounded-md bg-indigo-600 px-4 py-2 text-white shadow-sm hover:bg-indigo-500">
                                    {{ isEditMode ? 'Submit Changes' : 'Add Address' }}
                                </button>
                            </div>
                        </DialogPanel>
                    </TransitionChild>
                </div>
            </Dialog>
        </TransitionRoot>
    </div>
</template>

<script>
import AddressLookup from '@/components/Forms/Address Components/AddressLookup.vue';
import { Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot } from '@headlessui/vue';
import { XMarkIcon } from '@heroicons/vue/24/outline';
import axios from 'axios';
import { inject, provide, ref } from 'vue';
import { useStore } from 'vuex';

    export default {
        components: {
            AddressLookup,
            TransitionRoot,
            TransitionChild,
            Dialog,
            DialogPanel,
            DialogTitle,
            XMarkIcon
        },
        setup() {
            const address = inject('address');

            const addressLookupQuery = ref('');
            const addressSuggestions = ref([]);
            const zipcodeErrMsg = ref('');
            const states = ref([
                "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
                "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
                "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
                "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
                "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
            ]);
            const store = useStore();

            const countries = ref(["US", "CA", "MX", "UK"]);
            const isAddressModalOpen = inject('isAddressModalOpen');
            const closeAddressModal = inject('closeAddressModal');
            const businessId = inject('businessId');
            const modalTitle = inject('modalTitle');
            const fetchBusinessData = inject('fetchBusinessData');
            const addressIds = inject('addressIds');
            const openAddModal = inject('openAddModal');
            const isEditMode = inject('isEditMode');
            const addressData = inject('addressData');
            const selectedIndex = inject('selectedIndex');
            const formErrMsg = inject('formErrMsg');

            const inputClass = (errorMsg) => {
                return [
                'block w-full rounded-md border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                errorMsg ? 'border-red-500' : ''
                ];
            };

            const addAddress = async () => {
                console.log("calling addAddress method");
                try {
                    const csrf_access = store.getters['accounts/getAccessCSRF'];
                    const newAddress = { line1: address.value.line1, line2: address.value.line2, city: address.value.city, state: address.value.state, zipcode: address.value.zipcode, country: address.value.country };

                    const response = await axios.post(`https://localhost:5000/add_address/${businessId.value}`, 
                                          { address: newAddress },
                                          { 
                                            headers: {
                                                'X-CSRF-TOKEN': csrf_access
                                            },
                                            withCredentials: true 
                                          });
                    console.log(response.data);
                    fetchBusinessData();
                    closeAddressModal();
                } catch (error) {
                    if (error.response && error.response.data && error.response.data.error) {
                        const errorMsg = error.response.data.error.replace(/['"]+/g, '').replace(/&quot;/g, '');
                        if (errorMsg.includes('zipcode')) {
                            zipcodeErrMsg.value = errorMsg;
                        }
                        else {
                            formErrMsg.value = errorMsg;
                        }
                    } else {
                        formErrMsg.value = 'Network error. Please try again later.';
                    }
                    console.error('Error adding business:', error);
                }
            };

            const editAddress = async () => {
                formErrMsg.value = '';
                zipcodeErrMsg.value = '';

                console.log("calling editAddress method");
                const addressId = addressIds.value[selectedIndex.value];
                const editedAddressData = address.value;
                console.log("address data edited: ", address.value);

                try {
                    const response = await axios.put(`https://localhost:5000/edit_address/${addressId}`, editedAddressData, { withCredentials: true });
                    console.log(response.data);
                    console.log("Address updated successfully");
                    fetchBusinessData();
                    closeAddressModal();
                } catch (error) {
                    if (error.response && error.response.data && error.response.data.error) {
                        const errorMsg = error.response.data.error.replace(/['"]+/g, '').replace(/&quot;/g, '');
                        if (errorMsg.includes('zipcode')) {
                            zipcodeErrMsg.value = errorMsg;
                        }
                        else {
                            formErrMsg.value = errorMsg;
                        }
                    } else {
                        formErrMsg.value = 'Network error. Please try again later.';
                    }
                    console.error('Error adding business:', error);
                }
            };

            const handleAddressAction = () => {
                if (isEditMode.value) {
                    editAddress();
                } else {
                    addAddress();
                }
            };

            provide('address', address);
            provide('addressLookupQuery', addressLookupQuery);
            provide('addressSuggestions', addressSuggestions);
            provide('zipcodeErrMsg', zipcodeErrMsg);
            provide('states', states);
            provide('countries', countries);
            provide('inputClass', inputClass);
            
            return {
                address,
                addressLookupQuery,
                addressSuggestions,
                zipcodeErrMsg,
                states,
                countries,
                inputClass,
                isAddressModalOpen,
                closeAddressModal,
                businessId,
                addAddress,
                store,
                isEditMode,
                modalTitle,
                openAddModal,
                editAddress,
                addressData,
                selectedIndex,
                handleAddressAction,
                formErrMsg
            };
        }
    }

</script>

<style>
</style>