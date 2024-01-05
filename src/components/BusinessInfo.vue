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
        <EditBusinessButton></EditBusinessButton>
    </div>
</template>  

<script>
import { computed, provide, ref } from 'vue';
import { useRoute } from 'vue-router';
import EditBusinessButton from './Data Display/Info Table Components/EditBusinessButton.vue';
import PrintReport from './Data Display/Info Table Components/PrintReport.vue';
import TableDisplay from './Data Display/Info Table Components/TableDisplay.vue';
import DarkModeSwitch from './UI Enhancements/DarkModeSwitch.vue';

export default {
  components: {
    PrintReport,
    TableDisplay,
    DarkModeSwitch,
    EditBusinessButton
  },
  setup() {
    const businessData = ref({});
    const addressData = ref([]);
    const businessName = ref('');
    const businessId = ref(null);
    const route = useRoute();
    const isDialogOpen = ref(false);
    const mapEmbedUrl = ref('');
    const isEditing = ref(false);
    const editedData = ref({});
    const isExpanded = ref(false);
    const isAdmin = ref(false);
    const yearlyRevenueError = ref('');
    const employeeCountError = ref('');
    const websiteTrafficError = ref('');
    const floatError = ref('');
    const keys = ref(["Business ID", "Phone Number", "Has Resources Available?", "Organization Type", "Types of Resources"]);
    const adminKeys = ref(["Yearly Revenue", "Employee Count", "Customer Satisfaction", "Website Traffic"]);
    const adminFieldMapping = {
      "Yearly Revenue": "yearly_revenue",
      "Employee Count": "employee_count",
      "Customer Satisfaction": "customer_satisfaction",
      "Website Traffic": "website_traffic"
    };

    const mapping = {
      "Business ID": "business_id",
      "Phone Number": "contact_info",
      "Has Resources Available?": "has_available_resources",
      "Organization Type": "organization_type",
      "Types of Resources": "resources_available"
    };

    const displayKeys = computed(() => {
        let keysArray = keys.value.map(key => ({ label: key, value: mapping[key] }));

        if (isAdmin.value) {
            const adminKeysArray = adminKeys.value.map(key => ({ label: key, value: adminFieldMapping[key] }));
            keysArray = keysArray.concat(adminKeysArray);
        }

        return keysArray;
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

    const formattedAddresses = computed(() => {
        return addressData.value.map(addr => {
            return [
                addr.line1, addr.city, addr.state, addr.zipcode, addr.country
            ].filter(Boolean).join(", ");
        });
    });

    const formattedContactInfo = computed({
      get: () => {
        return formatPhoneNumber(businessData.value.contact_info);
      },
      set: (newValue) => {
        businessData.value.contact_info = unformatPhoneNumber(newValue);
      }
    });

    const openModal = () => {
        if (formattedAddresses.value) {
            const encodedAddress = encodeURIComponent(formattedAddresses.value);
            mapEmbedUrl.value = `https://maps.google.com/maps?q=${encodedAddress}&t=&z=13&ie=UTF8&iwloc=&output=embed`;
        }
        isDialogOpen.value = true;
    };

    function formatPhoneNumber(value) {
        if (!value) {
            return '';
        }

        const phoneNumber = value.replace(/[^\d]/g, '');
        if (phoneNumber.length < 4) {
            return phoneNumber;
        }
        if (phoneNumber.length < 7) {
            return `${phoneNumber.slice(0, 3)}-${phoneNumber.slice(3)}`;
        }
        
        return `${phoneNumber.slice(0, 3)}-${phoneNumber.slice(3, 6)}-${phoneNumber.slice(6, 10)}`;
    }

    function unformatPhoneNumber(formattedValue) {
        return formattedValue.replace(/[^\d]/g, '');
    }

    const inputClass = (error) => {
        return [
            'input-edit -my-10 text-sm dark:bg-gray-700 dark:text-white dark:border-white border-1 w-full',
            error ? 'border-red-500' : ''
        ];
    };

    provide('businessData', businessData);
    provide('addressData', addressData)
    provide('businessName', businessName);
    provide('businessId', businessId);
    provide('keys', keys);
    provide('route', route);
    provide('isDialogOpen', isDialogOpen);
    provide('mapEmbedUrl', mapEmbedUrl);
    provide('isExpanded', isExpanded);
    provide('isAdmin', isAdmin);
    provide('adminKeys', adminKeys);
    provide('displayKeys', displayKeys)
    provide('adminFieldMapping', adminFieldMapping);
    provide('mapping', mapping);
    provide('formattedResourcesAvailable', formattedResourcesAvailable);
    provide('formattedAvailability', formattedAvailability);
    provide('formattedAddresses', formattedAddresses);
    provide('openModal', openModal);
    provide('isEditing', isEditing);
    provide('editedData', editedData);
    provide('formattedContactInfo', formattedContactInfo);
    provide('formatPhoneNumber', formatPhoneNumber);
    provide('unformatPhoneNumber', unformatPhoneNumber);
    provide('yearlyRevenueError', yearlyRevenueError);
    provide('employeeCountError', employeeCountError);
    provide('websiteTrafficError', websiteTrafficError);
    provide('floatError', floatError);
    provide('inputClass', inputClass);

    return {
        businessData,
        addressData,
        businessName,
        businessId,
        keys,
        mapping,
        formattedAvailability,
        formattedResourcesAvailable,
        isDialogOpen,
        mapEmbedUrl,
        isExpanded,
        formattedAddresses,
        isAdmin,
        adminFieldMapping,
        adminKeys,
        openModal,
        isEditing,
        editedData,
        displayKeys,
        formattedContactInfo,
        formatPhoneNumber,
        unformatPhoneNumber,
        yearlyRevenueError,
        employeeCountError,
        websiteTrafficError,
        floatError
    };
  }
};
</script>

<style scoped>
</style>