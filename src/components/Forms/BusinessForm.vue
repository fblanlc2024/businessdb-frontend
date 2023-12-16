<template>
  <div class="space-y-6">
    <h2 class="text-2xl font-bold text-gray-900 text-center mt-5">Add New Business Client</h2>

    <!-- Business Name -->
    <BusinessName></BusinessName>

    <!-- Address Lookup -->
    <AddressLookup></AddressLookup>

    <!-- Organization Type -->
    <OrganizationType></OrganizationType>

    <!-- Resources Available -->
    <ResourcesAvailable></ResourcesAvailable>

    <!-- Has Available Resources -->
    <HasAvailableResources></HasAvailableResources>

    <!-- Contact Info -->
    <ContactInfo></ContactInfo>

    <AddBusinessButton></AddBusinessButton>
  </div>
</template>
  
<script>
import { computed, provide, ref } from 'vue';
import AddBusinessButton from './Business Form Components/AddBusinessButton.vue';
import AddressLookup from './Business Form Components/AddressLookup.vue';
import BusinessName from './Business Form Components/BusinessName.vue';
import ContactInfo from './Business Form Components/ContactInfo.vue';
import HasAvailableResources from './Business Form Components/HasAvailableResources.vue';
import OrganizationType from './Business Form Components/OrganizationType.vue';
import ResourcesAvailable from './Business Form Components/ResourcesAvailable.vue';

  export default {
    components: {
      AddBusinessButton,
      AddressLookup,
      BusinessName,
      ContactInfo,
      HasAvailableResources,
      OrganizationType,
      ResourcesAvailable
    },
    setup() {
      const addressLookupQuery = ref('');
      const addressSuggestions = ref([]);
      const zipcodeErrMsg = ref('');
      const addressErrMsg = ref('');
      const businessName = ref('');
      const contactInfo = ref('');
      const hasAvailableResources = ref('');
      const organizationType = ref('');
      const resourcesAvailable = ref('');
      const address = ref({
        number: '',
        street: '',
        city: '',
        state: '',
        zipcode: '',
        country: ''
      });

      const states = ref([
        "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
        "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
        "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
        "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
        "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
      ]);
      const countries = ref(["US, CA, MX"]);


      const hasAvailableResourcesBoolean = computed({
        get: () => hasAvailableResources.value === 'true',
        set: (newValue) => {
          hasAvailableResources.value = newValue ? 'true' : 'false';
        }
      });

      provide('address', address);
      provide('addressSuggestions', addressSuggestions);
      provide('addressErrMsg', addressErrMsg);
      provide('addressLookupQuery', addressLookupQuery)
      provide('zipcodeErrMsg', zipcodeErrMsg);
      provide('businessName', businessName);
      provide('contactInfo', contactInfo);
      provide('countries', countries);
      provide('hasAvailableResourcesBoolean', hasAvailableResourcesBoolean);
      provide('organizationType', organizationType);
      provide('resourcesAvailable', resourcesAvailable);
      provide('states', states);

      return {
        address,
        addressLookupQuery,
        addressSuggestions,
        zipcodeErrMsg,
        addressErrMsg,
        businessName,
        contactInfo,
        hasAvailableResources,
        hasAvailableResourcesBoolean,
        organizationType,
        resourcesAvailable,
        states,
        countries
      };
    }
  }
</script>

<style>
</style>