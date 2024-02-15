<template>
    <NavbarComponent />
    <ChatBotComponent />
    <div class="dark:bg-gray-800 dark:text-gray-400 min-h-screen">
        <div class="text-2xl font-bold mb-4 pt-6 text-center">
            <h2>Information for {{ businessName }}</h2>
        </div>
        <TableDisplay></TableDisplay>
        <PrintReport></PrintReport>
        <div class="col-start-2 text-center">
  </div>
        <AddressModal :isOpen="isAddressModalOpen" @close="closeAddressModal" />
        <DeleteAddressModal :isOpen="isDeleteModalOpen" @close="closeDeleteModal" />
    </div>
</template>  

<script>
import axios from 'axios';
import { computed, provide, ref } from 'vue';
import { useRoute } from 'vue-router';
import ChatBotComponent from '../Chatbot/ChatBotComponent.vue';
import AddressModal from '../Data Display/Info Table Components/AddressModal.vue';
import DeleteAddressModal from '../Data Display/Info Table Components/DeleteAddressModal.vue';
import PrintReport from '../Data Display/Info Table Components/PrintReport.vue';
import TableDisplay from '../Data Display/Info Table Components/TableDisplay.vue';
import NavbarComponent from '../UI Enhancements/NavbarComponent.vue';

export default {
  components: {
    PrintReport,
    TableDisplay,
    AddressModal,
    DeleteAddressModal,
    NavbarComponent,
    ChatBotComponent
},
  setup() {
    const addressData = ref([]);
    const addressIds = ref([]);
    const businessName = ref('');
    const businessData = ref({});
    const businessId = ref(null);
    const route = useRoute();
    const isDialogOpen = ref(false);
    const mapEmbedUrl = ref('');
    const isEditing = ref(false);
    const editedData = ref({});
    const isExpanded = ref(false);
    const isAdmin = ref(false);
    const isEditMode = ref(false);
    const yearlyRevenueError = ref('');
    const employeeCountError = ref('');
    const websiteTrafficError = ref('');
    const formErrMsg = ref('');
    const floatError = ref('');
    const isOpen = ref(false);
    const isAddressModalOpen = ref(false);
    const selectedIndex = ref(null);
    const isDeleteModalOpen = ref(false);
    const addressToDelete = ref(null);
    const modalTitle = ref('Add Address');
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

    const address = ref({
        line1: '',
        line2: '',
        city: '',
        state: '',
        zipcode: '',
        country: ''
    });

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
            (addr.address_line_1 !== undefined ? addr.address_line_1 : addr.line1),
             addr.line2, addr.city, addr.state, addr.zipcode, addr.country
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
                addressIds.value = responseData.addresses.map(address => address.address_id);
            } else {
                console.error('Address information not found');
            }
        } catch (error) {
            console.error('Error fetching business information:', error);
        }
    }

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
            '-my-10 text-sm dark:bg-gray-700 dark:text-white dark:border-white border-1 w-full',
            error ? 'border-red-500' : ''
        ];
    };

    const openAddressModal = () => {
        isAddressModalOpen.value = true;
    };

    const closeAddressModal = () => {
        isAddressModalOpen.value = false;
    };

    const openAddModal = () => {
        isEditMode.value = false;
        modalTitle.value = 'Add Address';
        address.value = { line1: '', line2: '', city: '', state: '', zipcode: '', country: '' };
        openAddressModal();  
    };

    const openEditModal = (index, addressInfo) => {
        isEditMode.value = true;
        modalTitle.value = 'Edit Address';
        selectedIndex.value = index;
        address.value = { 
            line1: (addressInfo.address_line_1 !== undefined ? addressInfo.address_line_1 : addressInfo.line1), 
            line2: addressInfo.line2, 
            city: addressInfo.city, 
            state: addressInfo.state, 
            zipcode: addressInfo.zipcode, 
            country: addressInfo.country 
        };
        openAddressModal();
    };

    const openDeleteModal = (index) => {
      console.log("Preparing to delete address with ID:", addressIds.value[index]);
      addressToDelete.value = addressIds.value[index];
      isDeleteModalOpen.value = true;
    };

    const closeDeleteModal = () => {
      isDeleteModalOpen.value = false;
      addressToDelete.value = null;
    };

    const confirmDelete = async () => {
      if (addressToDelete.value != null) {
        await axios.delete(`https://localhost:5000/delete_address/${addressToDelete.value}`, {withCredentials: true})
          .then(response => {
            console.log("Address deleted successfully", response);
            fetchBusinessData();
          })
          .catch(error => {
            console.error("Error deleting address", error);
          });
      }
      closeDeleteModal();
    };

    provide('businessData', businessData);
    provide('addressData', addressData);
    provide('address', address);
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
    provide('isAddressModalOpen', isAddressModalOpen);
    provide('openAddressModal', openAddressModal);
    provide('closeAddressModal', closeAddressModal);
    provide('addressIds', addressIds);
    provide('fetchBusinessData', fetchBusinessData);
    provide('isEditMode', isEditMode);
    provide('openAddModal', openAddModal);
    provide('openEditModal', openEditModal);
    provide('modalTitle', modalTitle);
    provide('selectedIndex', selectedIndex);
    provide('openDeleteModal', openDeleteModal);
    provide('isDeleteModalOpen', isDeleteModalOpen);
    provide('addressToDelete', addressToDelete);
    provide('closeDeleteModal', closeDeleteModal);
    provide('confirmDelete', confirmDelete);
    provide('formErrMsg', formErrMsg);

    return {
        businessData,
        businessName,
        businessId,
        keys,
        mapping,
        formErrMsg,
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
        floatError,
        isOpen,
        openAddressModal,
        closeAddressModal,
        isAddressModalOpen,
        addressIds,
        fetchBusinessData,
        openEditModal,
        openAddModal,
        address,
        isEditMode,
        selectedIndex,
        modalTitle,
        isDeleteModalOpen,
        addressToDelete,
        openDeleteModal,
        closeDeleteModal,
        confirmDelete
    };
  }
};
</script>

<style scoped>
</style>