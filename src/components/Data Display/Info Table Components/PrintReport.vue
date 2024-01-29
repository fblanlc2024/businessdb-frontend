<template>
    <div class="non-printing text-center mb-4">
        <button @click="generatePDF" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition">
            Print Report
        </button>
    </div>
</template>

<script>
import axios from 'axios';
import { inject, ref } from 'vue';

export default {
    setup() {
        const isAdmin = inject('isAdmin');
        const businessData = inject('businessData');
        const formattedAddresses = inject('formattedAddresses');
        const formattedResourcesAvailable = inject('formattedResourcesAvailable');
        const formattedContactInfo = inject('formattedContactInfo');
        const modifiedBusinessData = ref([]);

        const generatePDF = () => {
            const isAdminStatus = isAdmin.value ? 'true' : 'false';
            modifiedBusinessData.value = JSON.parse(JSON.stringify(businessData.value));

            modifiedBusinessData.value.resources_available = formattedResourcesAvailable.value;
            modifiedBusinessData.value.contact_info = formattedContactInfo.value;

            const payload = {
                isAdmin: isAdminStatus,
                businessData: modifiedBusinessData.value,
                formattedAddresses: formattedAddresses.value
            };

            const newTab = window.open('', '_blank');

            axios.post('https://localhost:5000/print_business_info', payload, { responseType: 'blob' })
            .then(response => {
                const blobUrl = window.URL.createObjectURL(new Blob([response.data]));
                
                if (newTab) {
                    newTab.location.href = blobUrl;
                } else {
                    console.error('Popup blocked');
                }
            })
            .catch(error => {
                console.error('There was an error!', error);
                if (newTab) newTab.close();
            });
        };

        return {
            generatePDF,
            isAdmin,
            businessData,
            formattedAddresses,
            formattedResourcesAvailable,
            formattedContactInfo,
            modifiedBusinessData
        }
    }
}
</script>

<style></style>