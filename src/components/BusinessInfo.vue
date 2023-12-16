<template>
    <div class="dark:bg-gray-800 dark:text-gray-400 min-h-screen">
        <!-- Header and Title -->
        <div
            class="non-printing flex justify-between items-center mb-4 py-5 pb-5 border-b-2 border-gray-400 text-center dark:border-gray-700">
            <div class="flex-1"></div>
            <h1 class="non-printing text-4xl font-bold flex-shrink">Business Info</h1>
            <DarkModeSwitch class="non-printing"></DarkModeSwitch>
        </div>

        <div class="text-2xl font-bold mb-4 pt-6 text-center">
            <h2>Information for {{ businessName }}</h2>
        </div>
        <TableDisplay></TableDisplay>
        <PrintReport></PrintReport>
    </div>
    <MapDisplay></MapDisplay>
</template>  

<script>
import { computed, provide, ref } from 'vue';
import { useRoute } from 'vue-router';
import MapDisplay from './Data Display/Info Table Components/MapDisplay.vue';
import PrintReport from './Data Display/Info Table Components/PrintReport.vue';
import TableDisplay from './Data Display/Info Table Components/TableDisplay.vue';
import DarkModeSwitch from './UI Enhancements/DarkModeSwitch.vue';

export default {
  components: {
    MapDisplay,
    PrintReport,
    TableDisplay,
    DarkModeSwitch
  },
  setup() {
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

    const openModal = () => {
        if (formattedAddress.value) {
            const encodedAddress = encodeURIComponent(formattedAddress.value);
            mapEmbedUrl.value = `https://maps.google.com/maps?q=${encodedAddress}&t=&z=13&ie=UTF8&iwloc=&output=embed`;
        }
        isDialogOpen.value = true;
    };

    provide('businessData', businessData);
    provide('businessName', businessName);
    provide('keys', keys);
    provide('route', route);
    provide('isDialogOpen', isDialogOpen);
    provide('mapEmbedUrl', mapEmbedUrl);
    provide('isExpanded', isExpanded);
    provide('isAdmin', isAdmin);
    provide('adminFields', adminFields);
    provide('adminFieldMapping', adminFieldMapping);
    provide('mapping', mapping);
    provide('formattedResourcesAvailable', formattedResourcesAvailable);
    provide('formattedAvailability', formattedAvailability);
    provide('formattedAddress', formattedAddress);
    provide('openModal', openModal);

    return {
        businessData,
        businessName,
        keys,
        mapping,
        formattedAvailability,
        formattedResourcesAvailable,
        isDialogOpen,
        mapEmbedUrl,
        isExpanded,
        formattedAddress,
        isAdmin,
        adminFieldMapping,
        adminFields,
        openModal
    };
  }
};
</script>

<style scoped>
</style>