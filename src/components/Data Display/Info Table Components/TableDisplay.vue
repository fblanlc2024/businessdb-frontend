<template>
    <div class="max-w-4xl mx-auto overflow-hidden bg-white shadow-lg rounded-lg dark:bg-gray-800 mt-8 mb-8">
        <div class="data-display-for-print divide-y divide-gray-200 dark:divide-gray-700">
            <div v-for="displayName in keys" :key="displayName" class="grid grid-cols-2">
                <div class="px-6 py-4 text-sm font-medium text-gray-900 dark:text-white whitespace-normal border-r border-gray-200 dark:border-gray-700">
                    {{ displayName }}
                </div>
                <div :class="['px-6 py-4 text-sm text-gray-500 dark:text-gray-400 whitespace-normal', 'border-gray-200 dark:border-gray-700']">
                    <template v-if="!isEditing">
                        <!-- Display the value -->
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
                    </template>
                    <template v-else>
                        <!-- Show input field when in edit mode -->
                        <input type="text" v-model="editedData[mapping[displayName]]" class="w-full px-2 py-1 border rounded">
                    </template>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import { inject, onMounted } from 'vue';

export default {
  setup() {
    const businessData = inject('businessData');
    const businessName = inject('businessName');
    const keys = inject('keys');
    const route = inject('route');
    const isDialogOpen = inject('isDialogOpen');
    const mapEmbedUrl = inject('mapEmbedUrl');
    const isExpanded = inject('isExpanded');
    const isAdmin = inject('isAdmin');
    const mapping = inject('mapping');
    const adminFields = inject('adminFields');
    const adminFieldMapping = inject('adminFieldMapping');
    const formattedResourcesAvailable = inject('formattedResourcesAvailable');
    const formattedAvailability = inject('formattedAvailability');
    const formattedAddress = inject('formattedAddress');
    const openModal = inject('openModal');
    const isEditing = inject('isEditing');
    const editedData = inject('editedData');

    onMounted(async () => {
        businessName.value = route.query.businessName;
        const { checkAdminStatus } = await import('../../utils/adminCheck');
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

    return {
        businessData,
        businessName,
        keys,
        formattedAvailability,
        formattedResourcesAvailable,
        isDialogOpen,
        mapEmbedUrl,
        isExpanded,
        formattedAddress,
        isAdmin,
        adminFieldMapping,
        adminFields,
        mapping,
        openModal,
        isEditing,
        editedData
    };
  }
};
</script>

<style>
</style>