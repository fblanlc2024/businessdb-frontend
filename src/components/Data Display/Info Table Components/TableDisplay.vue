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
                        <!-- Input Field Mode -->
                        <div v-if="item.value === 'has_available_resources' && isEditing" class="-my-2">
                            <select v-model="editedData[item.value]" class="custom-select">
                                <option value="true">Yes</option>
                                <option value="false">No</option>
                            </select>
                        </div>
                        <div v-else-if="item.value === 'contact_info'">
                            <input
                                class="-my-10 dark:bg-gray-700 dark:text-white dark:border-white border-1 w-full text-sm"
                                type="text" v-model="formattedContactInfo"/>
                        </div>
                        <div v-else-if="item.value === 'customer_satisfaction'">
                            <input
                                :class="['-my-10 text-sm', 'dark:bg-gray-700 dark:text-white dark:border-white border-1 w-full']"
                                :style="{borderColor: floatError ? 'red' : ''}"
                                type="text"
                                v-model="editedData['customer_satisfaction']"
                            />
                            <p v-if="floatError" class="text-red-500 text-xs mt-3 -my-3">{{ floatError }}</p>
                        </div>
                        <div v-else-if="item.value === 'yearly_revenue'">
                            <input 
                                :class="['-my-10 text-sm', 'dark:bg-gray-700 dark:text-white dark:border-white border-1 w-full']"
                                :style="{borderColor: yearlyRevenueError ? 'red' : ''}"
                                type="text" 
                                v-model="editedData['yearly_revenue']" 
                            />
                            <p v-if="yearlyRevenueError" class="text-red-500 text-xs mt-3 -my-3">{{ yearlyRevenueError }}</p>
                        </div>

                        <div v-else-if="item.value === 'employee_count'">
                            <input 
                                :class="['-my-10 text-sm', 'dark:bg-gray-700 dark:text-white dark:border-white border-1 w-full']"
                                :style="{borderColor: employeeCountError ? 'red' : ''}"
                                type="text" 
                                v-model="editedData['employee_count']" 
                            />
                            <p v-if="employeeCountError" class="text-red-500 text-xs mt-3 -my-3">{{ employeeCountError }}</p>
                        </div>

                        <div v-else-if="item.value === 'website_traffic'">
                            <input 
                                :class="['-my-10 text-sm', 'dark:bg-gray-700 dark:text-white dark:border-white border-1 w-full']"
                                :style="{borderColor: websiteTrafficError ? 'red' : ''}"
                                type="text" 
                                v-model="editedData['website_traffic']" 
                            />
                            <p v-if="websiteTrafficError" class="text-red-500 text-xs mt-1 -my-3">{{ websiteTrafficError }}</p>
                        </div>
                        <input 
                            v-else 
                            type="text" 
                            v-model="editedData[item.value]" 
                            class="-my-10 text-sm dark:bg-gray-700 dark:text-white dark:border-white border-1 w-full"
                        >
                    </template>
                </div>
            </div>
            <EditBusinessButton></EditBusinessButton>
        </div>
    </div>

    <div v-if="formattedAddresses.length > 0" class="max-w-4xl mx-auto overflow-hidden bg-white shadow-lg rounded-lg dark:bg-gray-800 mt-8 mb-8">
        <h3 class="px-6 py-4 text-lg font-medium text-gray-900 dark:text-white">Addresses</h3>
        <div class="data-display-for-print divide-y divide-gray-200 dark:divide-gray-700">
            <div v-for="(address, index) in formattedAddresses" :key="index" class="grid grid-cols-2 items-center">
                <div class="px-6 py-4 text-sm font-medium text-gray-900 dark:text-white whitespace-normal border-r border-gray-200 dark:border-gray-700">
                    Address {{ index + 1 }}
                </div>
                <div 
                    :class="['px-6 py-4 text-sm text-gray-500 dark:text-gray-400 whitespace-normal flex justify-between items-center', 'cursor-pointer hover:underline', 'border-gray-200 dark:border-gray-700', 'group']"
                    @click="openModal(address)"
                >
                    {{ address }}
                    <span class="hidden group-hover:flex space-x-2">
                        <PencilIcon class="h-6 w-6 text-blue-500 hover:text-blue-700 cursor-pointer -my-2" @click.stop="openEditModal(index, addressData[index])"/>
                        <TrashIcon class="h-6 w-6 text-red-500 hover:text-red-700 cursor-pointer -my-2" @click.stop="openDeleteModal(index)"/>
                    </span>
                </div>
            </div>
            <div @click="openAddModal()" class="bg-gray-800 hover:bg-gray-700 text-white font-bold py-3 px-2 text-center w-full">Add Address</div>
        </div>
    </div>
    <MapDisplay />
</template>

<script>
import { PencilIcon, TrashIcon } from '@heroicons/vue/24/outline';
import { inject, onMounted } from 'vue';
import MapDisplay from '../Info Table Components/MapDisplay.vue';
import EditBusinessButton from './EditBusinessButton.vue';

export default {
    components: {
        MapDisplay,
        PencilIcon,
        TrashIcon,
        EditBusinessButton
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
    const addressIds = inject('addressIds');
    const fetchBusinessData = inject('fetchBusinessData');
    const openEditModal = inject('openEditModal');
    const openDeleteModal = inject('openDeleteModal');
    const openAddModal = inject('openAddModal');

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
        inputClass,
        addressIds,
        openEditModal,
        openDeleteModal,
        openAddModal
    };
  }
};
</script>

<style>
/* Dark mode styling */
.dark .custom-select {
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

.dark .custom-select option {
  background-color: #374151; /* Same as select for consistency */
  color: white; /* Same as select for readability */
  padding: 0.5rem 1rem; /* Same padding as the select, but may not be applied in all browsers */
}

/* Light mode styling */
.custom-select {
  background-color: white; /* Light mode background color */
  color: #374151; /* Text color for light mode */
  border: 1px solid #374151;
  border-radius: 0.25rem;
  padding: 0.25rem 0.75rem; /* Adjust padding to match the input height */
  width: 100%; /* Full width */
  -webkit-appearance: none; /* Removes default styling on iOS */
  -moz-appearance: none; /* Removes default styling in Firefox */
  appearance: none; /* Removes default styling */
}

.custom-select option {
  background-color: white; /* Same as select for consistency */
  color: #374151; /* Same as select for readability */
  padding: 0.5rem 1rem; /* Same padding as the select, but may not be applied in all browsers */
}
</style>