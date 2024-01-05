<template>
    <div class="max-w-4xl mx-auto overflow-hidden bg-white shadow-lg rounded-lg dark:bg-gray-800 mt-8 mb-8">
        <div class="data-display-for-print divide-y divide-gray-200 dark:divide-gray-700">
            <div v-for="item in displayKeys" :key="item.label" class="grid grid-cols-2 flex">
                <div class="px-6 py-4 text-sm font-medium text-gray-900 dark:text-white whitespace-normal border-r border-gray-200 dark:border-gray-700">
                    {{ item.label }}
                </div>
                <div class="px-6 py-4 text-sm text-gray-500 dark:text-gray-400 whitespace-normal border-gray-200 dark:border-gray-700">
                    <template v-if="!isEditing || item.label === 'Business ID'">
                        <!-- Special case handling -->
                        <template v-if="item.value === 'resources_available'">
                            {{ formattedResourcesAvailable }}
                        </template>
                        <template v-else-if="item.value === 'has_available_resources'">
                            {{ formattedAvailability }}
                        </template>
                        <template v-else-if="item.value === 'contact_info'">
                            {{ formattedContactInfo }}
                        </template>
                        <template v-else>
                            <!-- Display value for regular fields -->
                            {{ businessData[item.value] || 'N/A' }}
                        </template>
                    </template>
                    <template v-else>
                        <div v-if="item.value === 'has_available_resources' && isEditing" class="input-edit -my-2">
                            <select v-model="editedData[item.value]" class="custom-select">
                                <option value="true">Yes</option>
                                <option value="false">No</option>
                            </select>
                        </div>
                        <div v-else-if="item.value === 'contact_info'">
                            <input
                                class="dark:bg-gray-700 dark:text-white dark:border-white border-1 w-full"
                                type="text" v-model="formattedContactInfo"/>
                        </div>
                        <div v-else-if="item.value === 'customer_satisfaction'">
                            <input
                                :class="['input-edit text-sm', inputClass(floatError), 'dark:bg-gray-700 dark:text-white dark:border-white border-1 w-full']"
                                type="text"
                                v-model="editedData['customer_satisfaction']"
                            />
                            <p v-if="floatError" class="text-red-500 text-xs mt-3 -mb-3">{{ floatError }}</p>
                        </div>
                        <div v-else-if="item.value === 'yearly_revenue'">
                            <input 
                                :class="['input-edit text-sm', inputClass(yearlyRevenueError), 'dark:bg-gray-700 dark:text-white dark:border-white border-1 w-full']"
                                type="text" 
                                v-model="editedData['yearly_revenue']" 
                            />
                            <p v-if="yearlyRevenueError" class="text-red-500 text-xs mt-3 -mb-3">{{ yearlyRevenueError }}</p>
                        </div>

                        <div v-else-if="item.value === 'employee_count'">
                            <input 
                                :class="['input-edit text-sm', inputClass(employeeCountError), 'dark:bg-gray-700 dark:text-white dark:border-white border-1 w-full']"
                                type="text" 
                                v-model="editedData['employee_count']" 
                            />
                            <p v-if="employeeCountError" class="text-red-500 text-xs mt-3 -mb-3">{{ employeeCountError }}</p>
                        </div>

                        <div v-else-if="item.value === 'website_traffic'">
                            <input 
                                :class="['input-edit text-sm', inputClass(websiteTrafficError), 'dark:bg-gray-700 dark:text-white dark:border-white border-1 w-full']"
                                type="text" 
                                v-model="editedData['website_traffic']" 
                            />
                            <p v-if="websiteTrafficError" class="text-red-500 text-xs mt-3 -mb-3">{{ websiteTrafficError }}</p>
                        </div>
                        <input 
                            v-else 
                            type="text" 
                            v-model="editedData[item.value]" 
                            class="input-edit -my-10 text-sm dark:bg-gray-700 dark:text-white dark:border-white border-1 w-full"
                        >
                    </template>
                </div>
            </div>
        </div>
    </div>

    <div v-if="formattedAddresses.length > 0" class="max-w-4xl mx-auto overflow-hidden bg-white shadow-lg rounded-lg dark:bg-gray-800 mt-8 mb-8">
        <h3 class="px-6 py-4 text-lg font-medium text-gray-900 dark:text-white">Addresses</h3>
        <div class="data-display-for-print divide-y divide-gray-200 dark:divide-gray-700">
            <div v-for="(address, index) in formattedAddresses" :key="index" class="grid grid-cols-2">
                <div class="px-6 py-4 text-sm font-medium text-gray-900 dark:text-white whitespace-normal border-r border-gray-200 dark:border-gray-700">
                    Address {{ index + 1 }}
                </div>
                <div class="px-6 py-4 text-sm text-gray-500 dark:text-gray-400 whitespace-normal border-gray-200 dark:border-gray-700">
                    {{ address }}
                </div>
            </div>
        </div>
    </div>
    <MapDisplay />
</template>

<script>
import axios from 'axios';
import { inject, onMounted } from 'vue';
import MapDisplay from '../Info Table Components/MapDisplay.vue';

export default {
    components: {
        MapDisplay
    },
  setup() {
    const businessData = inject('businessData');
    const addressData = inject('addressData');
    const businessName = inject('businessName');
    const businessId = inject('businessId');
    const keys = inject('keys');
    const route = inject('route');
    const isDialogOpen = inject('isDialogOpen');
    const mapEmbedUrl = inject('mapEmbedUrl');
    const isExpanded = inject('isExpanded');
    const isAdmin = inject('isAdmin');
    const mapping = inject('mapping');
    const adminKeys = inject('adminKeys');
    const displayKeys = inject('displayKeys');
    const adminFieldMapping = inject('adminFieldMapping');
    const formattedResourcesAvailable = inject('formattedResourcesAvailable');
    const formattedAvailability = inject('formattedAvailability');
    const formattedAddresses = inject('formattedAddresses');
    const openModal = inject('openModal');
    const isEditing = inject('isEditing');
    const editedData = inject('editedData');
    const formattedContactInfo = inject('formattedContactInfo');
    const unformatPhoneNumber = inject('unformatPhoneNumber');
    const yearlyRevenueError = inject('yearlyRevenueError');
    const employeeCountError = inject('employeeCountError');
    const websiteTrafficError = inject('websiteTrafficError');
    const floatError = inject('floatError');
    const inputClass = inject('inputClass');

    onMounted(async () => {
        businessName.value = route.query.businessName;
        const { checkAdminStatus } = await import('../../utils/adminCheck');
        isAdmin.value = await checkAdminStatus();

        if (businessName.value) {
            fetchBusinessData();

        } else {
            console.error('Business name not provided in query');
        }
    });

    const fetchBusinessData = async () => {
        try {
            const response = await axios.get(`https://localhost:5000/api/business_info?name=${encodeURIComponent(businessName.value)}`, {withCredentials: true});
            console.log(response.data);

            const responseData = response.data;

            if (responseData.business_info) {
                businessData.value = responseData.business_info;
                businessId.value = responseData.business_info.business_id;
                console.log("business id value: " + businessId.value);
            } else {
                console.error('Business information not found');
            }

            if (responseData.addresses && responseData.addresses.length > 0) {
                addressData.value = responseData.addresses;
            } else {
                console.error('Address information not found');
            }
        } catch (error) {
            console.error('Error fetching business information:', error);
        }
    }



    return {
        businessData,
        addressData,
        businessName,
        keys,
        formattedAvailability,
        formattedResourcesAvailable,
        isDialogOpen,
        mapEmbedUrl,
        isExpanded,
        isAdmin,
        adminFieldMapping,
        adminKeys,
        mapping,
        openModal,
        isEditing,
        editedData,
        formattedAddresses,
        fetchBusinessData,
        displayKeys,
        businessId,
        formattedContactInfo,
        unformatPhoneNumber,
        yearlyRevenueError,
        employeeCountError,
        websiteTrafficError,
        floatError,
        inputClass
    };
  }
};
</script>

<style>
.custom-select {
  background-color: #374151; /* Dark mode background color */
  color: white; /* Text color for dark mode */
  border: 1px solid #ddd;
  border-radius: 0.25rem;
  padding: 0.25rem 0.75rem; /* Adjust padding to match the input height */
  width: 100%; /* Full width */
  -webkit-appearance: none; /* Removes default styling on iOS */
  -moz-appearance: none; /* Removes default styling in Firefox */
  appearance: none; /* Removes default styling */
}

/* Attempt to style the options */
.custom-select option {
  background-color: #374151; /* Same as select for consistency */
  color: white; /* Same as select for readability */
  padding: 0.5rem 1rem; /* Same padding as the select, but may not be applied in all browsers */
}
</style>