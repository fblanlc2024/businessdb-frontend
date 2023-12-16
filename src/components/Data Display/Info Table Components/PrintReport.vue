<template>
    <div class="non-printing text-center mb-4">
        <button @click="generatePDF" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition">
            Print Report
        </button>
    </div>
</template>

<script>
import { inject } from 'vue';

export default {
    setup() {
        const businessName = inject('businessName');
        const isAdmin = inject('isAdmin');

        const generatePDF = () => {
            const businessNameEncoded = encodeURIComponent(businessName.value);
            const isAdminStatus = isAdmin.value ? 'true' : 'false';

            window.open(`https://localhost:5000/print_business_info?name=${businessNameEncoded}&isAdmin=${isAdminStatus}`, '_blank');
        };

        return {
            generatePDF
        }
    }
}
</script>

<style></style>