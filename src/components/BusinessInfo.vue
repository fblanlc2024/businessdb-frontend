<template>
    <div class="dark:bg-gray-800 dark:text-gray-400 min-h-screen">
        <!-- Header and Title -->
        <div class="non-printing flex justify-between items-center mb-4 py-5 pb-5 border-b-2 border-gray-400 text-center dark:border-gray-700">
        <div class="flex-1"></div>
        <h1 class="non-printing text-4xl font-bold flex-shrink">Business Info</h1>
        <DarkModeSwitch class="non-printing"></DarkModeSwitch>
    </div>

        <div class="text-2xl font-bold mb-4 pt-6 text-center">
            <h2>Information for {{ businessName }}</h2>
        </div>

        <!-- Data Display using divs -->
        <div class="max-w-4xl mx-auto overflow-hidden bg-white shadow-lg rounded-lg dark:bg-gray-800 mt-8 mb-8">
            <div class="data-display-for-print divide-y divide-gray-200 dark:divide-gray-700">
                <div v-for="(displayName, index) in keys" :key="displayName" :class="{'grid grid-cols-2': !isAdmin, 'grid grid-cols-3': isAdmin}">
                    <div :class="['px-6 py-4 text-sm font-medium text-gray-900 dark:text-white whitespace-normal', isAdmin || index < keys.length ? 'border-r' : '', 'border-gray-200 dark:border-gray-700']">
                        {{ displayName }}
                    </div>
                    <div :class="['px-6 py-4 text-sm text-gray-500 dark:text-gray-400 whitespace-normal', isAdmin ? 'border-r' : '', mapping[displayName] === 'address' ? 'cursor-pointer hover:underline' : '', 'border-gray-200 dark:border-gray-700']" @click="mapping[displayName] === 'address' ? openModal(businessData.address) : null">
                        <template v-if="mapping[displayName] === 'resources_available'">
                            {{ formattedResourcesAvailable }}
                        </template>
                        <template v-else-if="mapping[displayName] === 'has_available_resources'">
                            {{ formattedAvailability }}
                        </template>
                        <template v-else-if="mapping[displayName] === 'address'">
                            {{ formattedAddress }}
                        </template>
                        <template v-else>
                            {{ businessData[mapping[displayName]] }}
                        </template>
                    </div>
                    <div v-if="isAdmin" class="px-6 py-4 border-gray-200 dark:border-gray-700 text-sm text-gray-500 dark:text-gray-400 whitespace-normal">
                        <button @click="editField(displayName)" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-1 px-2 rounded">
                            Edit
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <div class="non-printing text-center mb-4">
            <button @click="generatePDF" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition">
                Print Report
            </button>
        </div>
    </div>

    <TransitionRoot as="template" :show="isDialogOpen">
        <Dialog as="div" class="fixed inset-0 z-10 overflow-y-auto" @close="closeModal">
            <div class="flex items-end justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
                <TransitionChild as="template" enter="ease-out duration-300" enter-from="opacity-0" enter-to="opacity-100" leave="ease-in duration-200" leave-from="opacity-100" leave-to="opacity-0">
                    <DialogOverlay class="fixed inset-0 transition-opacity bg-black bg-opacity-50" />
                </TransitionChild>

                <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
                <TransitionChild as="template" enter="ease-out duration-300" enter-from="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95" enter-to="opacity-100 translate-y-0 sm:scale-100" leave="ease-in duration-200" leave-from="opacity-100 translate-y-0 sm:scale-100" leave-to="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95">
                    <DialogPanel :class="['inline-block align-bottom bg-white rounded-lg overflow-hidden shadow-xl transform transition-all sm:align-middle', isExpanded ? 'fixed inset-0 z-50 w-full h-full max-w-none p-0' : 'sm:my-8 sm:max-w-lg sm:w-full sm:p-6']">
                        <div class="absolute top-0 right-0 p-6 cursor-pointer hover-effect icon-container" @click="toggleModalSize">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 3.75v4.5m0-4.5h4.5m-4.5 0L9 9M3.75 20.25v-4.5m0 4.5h4.5m-4.5 0L9 15M20.25 3.75h-4.5m4.5 0v4.5m0-4.5L15 9m5.25 11.25h-4.5m4.5 0v-4.5m0 4.5L15 15" />
                            </svg>
                        </div>
                        <iframe :src="mapEmbedUrl" width="100%" :height="isExpanded ? '100%' : '500'" frameborder="0" allowfullscreen></iframe>
                    </DialogPanel>
                </TransitionChild>
            </div>
        </Dialog>
    </TransitionRoot>
</template>  

<script>
import { checkAdminStatus } from '@/adminCheck';
import { Dialog, DialogOverlay, DialogPanel, TransitionChild, TransitionRoot } from '@headlessui/vue';
import axios from 'axios';
import { computed, onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import DarkModeSwitch from './DarkModeSwitch.vue';

export default {
  components: {
    Dialog,
    DialogPanel,
    DialogOverlay,
    TransitionRoot,
    TransitionChild,
    DarkModeSwitch
  },
  setup() {
    const isDarkMode = ref(false);
    const businessData = ref({}); 
    const businessName = ref('');
    const keys = ref(["Address", "Business ID", "Contact Info", "Resources Available", "Organization Type", "Types of Resources"]);
    const route = useRoute();
    const isDialogOpen = ref(false);
    const mapEmbedUrl = ref('');
    const isExpanded = ref(false);
    const isAdmin = ref(false);
    const adminFields = ref(["Yearly Revenue", "Employee Count", "Customer Satisfaction", "Website Traffic"]);
    const adminFieldMapping = {
      "Yearly Revenue": "yearly_revenue",
      "Employee Count": "employee_count",
      "Customer Satisfaction": "customer_satisfaction",
      "Website Traffic": "website_traffic"
    };

    const mapping = {
      "Address": "address",
      "Business ID": "business_id",
      "Contact Info": "contact_info",
      "Resources Available": "has_available_resources",
      "Organization Type": "organization_type",
      "Types of Resources": "resources_available"
    };

    const openModal = () => {
        if (formattedAddress.value) {
            const encodedAddress = encodeURIComponent(formattedAddress.value);
            mapEmbedUrl.value = `https://maps.google.com/maps?q=${encodedAddress}&t=&z=13&ie=UTF8&iwloc=&output=embed`;
        }
        isDialogOpen.value = true;
    };

    const closeModal = () => {
        isDialogOpen.value = false;
    }

    const toggleModalSize = () => {
        isExpanded.value = !isExpanded.value;
    }

    const generatePDF = () => {
        const businessNameEncoded = encodeURIComponent(businessName.value);
        const isAdminStatus = isAdmin.value ? 'true' : 'false';

        window.open(`https://localhost:5000/print_business_info?name=${businessNameEncoded}&isAdmin=${isAdminStatus}`, '_blank');
    };  

    onMounted(async () => {
        businessName.value = route.query.businessName;
        isAdmin.value = await checkAdminStatus();

        if (businessName.value) {
            axios.get(`https://localhost:5000/api/business_info?name=${encodeURIComponent(businessName.value)}`)
            .then(response => {
                console.log(response);
                businessData.value = response.data;
            })
            .catch(error => console.error(error));
        } else {
            console.error('Business name not provided in query');
        }
    });

    const formattedResourcesAvailable = computed(() => {
        const resources = businessData.value && businessData.value.resources_available;

        if (Array.isArray(resources)) {
            return resources.join(", ");
        } else if (typeof resources === 'string') {
            return resources.split(',')
                        .map(s => s.trim())
                        .map(s => s.charAt(0).toUpperCase() + s.slice(1))
                        .join(', ');
        }

        return '';
    });



    const formattedAvailability = computed(() => {
        if (businessData.value && typeof businessData.value.has_available_resources === 'boolean') {
            return businessData.value.has_available_resources ? "Yes" : "No";
        }
        return '';
    });

    const formattedAddress = computed(() => {
        if (businessData.value && typeof businessData.value.address === 'object') {
            const addr = businessData.value.address;
            return [
                addr.number, addr.city, addr.state, addr.zipcode, addr.country
            ].filter(Boolean).join(", ");
        }
        return '';
    });

    return {
        isDarkMode,
        businessData,
        businessName,
        keys,
        mapping,
        formattedAvailability,
        formattedResourcesAvailable,
        isDialogOpen,
        mapEmbedUrl,
        isExpanded,
        openModal,
        closeModal,
        toggleModalSize,
        formattedAddress,
        generatePDF,
        isAdmin,
        adminFieldMapping,
        adminFields
    };
  }
};
</script>

<style scoped>
.icon-container {
    position: absolute;
    top: 10px;
    right: 10px;
    background-color: white;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 20;
    padding: 5px;
}

.icon-container:hover {
    transform: scale(1.1);
    transition: transform 0.3s ease-in-out;
}

.icon-container svg {
    fill: black;
    width: 30px;
    height: 30px;
    z-index: 30;
}

svg {
    color: black;
}
.whitespace-normal {
    white-space: normal;
    overflow-wrap: break-word;
    word-wrap: break-word;
    text-overflow: ellipsis;
    overflow: hidden;
    word-break: normal;
}
</style>