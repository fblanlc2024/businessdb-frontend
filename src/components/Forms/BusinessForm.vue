<template>
  <div class="space-y-6">
    <h2 class="text-2xl font-bold text-gray-900 text-center mt-5">Add New Business Client</h2>

    <!-- Business Name -->
    <div>
      <label for="businessName" class="block text-sm font-medium text-gray-900">Business Name</label>
      <input id="businessName" v-model="businessName" required placeholder="Enter business name" class="mt-2 block w-full rounded-md border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
    </div>

    <AddressLookup></AddressLookup>

    <!-- Organization Type -->
    <div>
      <label for="organizationType" class="block text-sm font-medium text-gray-900">Organization Type</label>
      <input id="organizationType" v-model="organizationType" required placeholder="Enter organization type" class="mt-2 block w-full rounded-md border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
    </div>

    <!-- Resources Available -->
    <div>
      <label for="resourcesAvailable" class="block text-sm font-medium text-gray-900">Resources Available</label>
      <input id="resourcesAvailable" v-model="resourcesAvailable" required placeholder="Enter available resources" class="mt-2 block w-full rounded-md border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
    </div>

    <!-- Has Available Resources -->
    <div>
      <label for="hasAvailableResources" class="block text-sm font-medium text-gray-900">Has Available Resources Right Now?</label>
      <select id="hasAvailableResources" v-model="hasAvailableResources" required class="mt-2 block w-full rounded-md border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" :class="{'selected-text': hasAvailableResources !== ''}">
        <option value="" disabled selected hidden>Select option</option>
        <option value="true">Yes</option>
        <option value="false">No</option>
      </select>
    </div>

    <!-- Contact Info -->
    <div>
      <label for="contactInfo" class="block text-sm font-medium text-gray-900">Contact Info</label>
      <input id="contactInfo" v-model="contactInfo" @input="formatPhoneNumber" required placeholder="Enter contact info" :class=inputClass(contactInfoErrMsg) />
      <p v-if="contactInfoErrMsg" class="text-red-500 text-xs">{{ contactInfoErrMsg }}</p>
    </div>


      <div>
        <label for="yearlyRevenue" class="block text-sm font-medium text-gray-900">Yearly Revenue</label>
        <input id="yearlyRevenue" v-model="yearlyRevenue" required placeholder="Enter yearly revenue" :class="inputClass(yearlyRevenueErrMsg)" />
        <p v-if="yearlyRevenueErrMsg" class="text-red-500 text-xs">{{ yearlyRevenueErrMsg }}</p>
      </div>
      <div>
        <label for="employeeCount" class="block text-sm font-medium text-gray-900">Employee Count</label>
        <input id="employeeCount" v-model="employeeCount" required placeholder="Enter employee count" :class="inputClass(employeeCountErrMsg)" />
        <p v-if="employeeCountErrMsg" class="text-red-500 text-xs">{{ employeeCountErrMsg }}</p>
      </div>
      <div>
        <label for="customerSatisfaction" class="block text-sm font-medium text-gray-900">Customer Satisfaction</label>
        <input id="customerSatisfaction" v-model="customerSatisfaction" required placeholder="Enter customer satisfaction" :class="inputClass(customerSatisfactionErrMsg)" />
        <p v-if="customerSatisfactionErrMsg" class="text-red-500 text-xs">{{ customerSatisfactionErrMsg }}</p>
      </div>
      <div>
        <label for="websiteTraffic" class="block text-sm font-medium text-gray-900">Website Traffic</label>
        <input id="websiteTraffic" v-model="websiteTraffic" required placeholder="Enter website traffic" :class="inputClass(websiteTrafficErrMsg)" />
        <p v-if="websiteTrafficErrMsg" class="text-red-500 text-xs">{{ websiteTrafficErrMsg }}</p>
      </div>
      <div>
        <p v-if="formErrMsg" class="text-sm text-red-600 mt-1 mb-2">{{ formErrMsg }}</p>
        <button @click="addBusiness" class="w-full rounded-md bg-indigo-600 px-3 py-2 text-white shadow-sm hover:bg-indigo-500">Add Business</button>
      </div>
  </div>


</template>
  
<script>
import axios from 'axios';
import { computed, inject, nextTick, provide, ref } from 'vue';
import EventBus from '../utils/eventBus';
import AddressLookup from './Address Components/AddressLookup.vue';

  export default {
    components: {
      AddressLookup
    },
    setup() {
      const address = ref({
            line1: '',
            line2: '',
            city: '',
            state: '',
            zipcode: '',
            country: ''
        });

      const addressLookupQuery = ref('');
      const addressSuggestions = ref([]);
      const zipcodeErrMsg = ref('');
      const states = ref([
          "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
      ]);
      
      const countries = ref(["US", "CA", "MX", "UK"]);
      const businessName = ref('');
      const contactInfo = ref('');
      const formErrMsg = ref('');
      const hasAvailableResources = ref('');
      const organizationType = ref('');
      const resourcesAvailable = ref('');
      const yearlyRevenue = ref('');
      const employeeCount = ref('');
      const customerSatisfaction = ref('');
      const websiteTraffic = ref('');
      const yearlyRevenueErrMsg = ref('');
      const employeeCountErrMsg = ref('');
      const websiteTrafficErrMsg = ref('');
      const customerSatisfactionErrMsg = ref('');
      const contactInfoErrMsg = ref('');

      const isAdmin = inject('isAdmin');

      const hasAvailableResourcesBoolean = computed({
        get: () => hasAvailableResources.value === 'true',
        set: (newValue) => {
          hasAvailableResources.value = newValue ? 'true' : 'false';
        }
      });

      const inputClass = (errorMsg) => {
        return [
          'block w-full rounded-md border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
          errorMsg ? 'border-red-500' : ''
        ];
      };

      const parseNumber = (value) => {
        const parsedInt = parseInt(value);
        if (!isNaN(parsedInt) && parsedInt.toString() === value.toString()) {
          return parsedInt;
        }
        return parseFloat(value);
      };

      const formatBooleanValue = (value) => {
        return value === 'true' || value === true ? 'Yes' : 'No';
      };

      const addBusiness = async () => {
          formErrMsg.value = '';
          zipcodeErrMsg.value = '';
          yearlyRevenueErrMsg.value = '';
          employeeCountErrMsg.value = '';
          websiteTrafficErrMsg.value = '';
          customerSatisfactionErrMsg.value = '';
          contactInfoErrMsg.value = '';

          const businessData = {
              business_name: businessName.value,
              address: {
                  line1: address.value.line1,
                  line2: address.value.line2,
                  city: address.value.city,
                  state: address.value.state,
                  zipcode: address.value.zipcode,
                  country: address.value.country
              },
              organization_type: organizationType.value,
              resources_available: resourcesAvailable.value,
              has_available_resources: hasAvailableResourcesBoolean.value,
              contact_info: unformatPhoneNumber(contactInfo.value),
              yearly_revenue: parseInt(yearlyRevenue.value),
              employee_count: parseInt(employeeCount.value),
              customer_satisfaction: parseNumber(customerSatisfaction.value),
              website_traffic: parseInt(websiteTraffic.value)
          };

          // Validate numeric fields
          if (isNaN(businessData.yearly_revenue)) {
              yearlyRevenueErrMsg.value = 'Yearly revenue must be a valid number.';
          }
          if (isNaN(businessData.employee_count)) {
              employeeCountErrMsg.value = 'Employee count must be a valid number.';
          }
          if (isNaN(businessData.customer_satisfaction)) {
              customerSatisfactionErrMsg.value = 'Customer satisfaction must be a valid number.';
          }
          if (isNaN(businessData.website_traffic)) {
              websiteTrafficErrMsg.value = 'Website traffic must be a valid number.';
          }

          // Check if any error messages were set
          if (yearlyRevenueErrMsg.value || employeeCountErrMsg.value || customerSatisfactionErrMsg.value || websiteTrafficErrMsg.value) {
              formErrMsg.value = 'Please correct the errors before submitting.';
              return;
          }

          try {
              const response = await axios.post('https://localhost:5000/add_business', businessData, { withCredentials: true });
              console.log(response.data);
              EventBus.emit('business-added', response.data);
              EventBus.emit('close-modal');
          } catch (error) {
              if (error.response && error.response.data && error.response.data.error) {
                  const errorMsg = error.response.data.error.replace(/['"]+/g, '').replace(/&quot;/g, '');
                  handleErrorMessage(errorMsg);
              } else {
                  formErrMsg.value = 'Network error. Please try again later.';
              }
              console.error('Error adding business:', error);
          }
      };

      const handleErrorMessage = (errorMsg) => {
        if (errorMsg.includes('yearly_revenue')) {
          yearlyRevenueErrMsg.value = errorMsg;
          scrollToField('yearlyRevenue');
        } else if (errorMsg.includes('employee_count')) {
          employeeCountErrMsg.value = errorMsg;
          scrollToField('employeeCount');
        } else if (errorMsg.includes('customer_satisfaction')) {
          customerSatisfactionErrMsg.value = errorMsg;
          scrollToField('customerSatisfaction');
        } else if (errorMsg.includes('website_traffic')) {
          websiteTrafficErrMsg.value = errorMsg;
          scrollToField('websiteTraffic');
        } else if (errorMsg.includes('phone number')) {
          contactInfoErrMsg.value = errorMsg;
          scrollToField('contactInfoErrMsg');
        } else {
          formErrMsg.value = errorMsg;
        }
      };

      const scrollToField = async (fieldName) => {
        await nextTick();
        const element = document.getElementById(fieldName);
        if (element) {
          element.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
      };

      const formatPhoneNumber = () => {
        let input = contactInfo.value;
        input = input.replace(/\D/g, ''); // Remove all non-numeric characters
        // Format as per desired pattern (e.g., (123) 456-7890)
        if (input.length <= 3) {
          input = `(${input}`;
        } else if (input.length <= 6) {
          input = `(${input.slice(0, 3)}) ${input.slice(3)}`;
        } else {
          input = `(${input.slice(0, 3)}) ${input.slice(3, 6)}-${input.slice(6, 10)}`;
        }
        contactInfo.value = input; // Update the reactive property
      };

      function unformatPhoneNumber(formattedValue) {
          return formattedValue.replace(/[^\d]/g, '');
      }

      provide('address', address);
      provide('addressLookupQuery', addressLookupQuery);
      provide('addressSuggestions', addressSuggestions);
      provide('zipcodeErrMsg', zipcodeErrMsg);
      provide('states', states);
      provide('countries', countries);
      provide('inputClass', inputClass);

      return {
        address,
        addressLookupQuery,
        addressSuggestions,
        zipcodeErrMsg,
        formErrMsg,
        businessName,
        contactInfo,
        hasAvailableResources,
        hasAvailableResourcesBoolean,
        organizationType,
        resourcesAvailable,
        states,
        countries,
        isAdmin,
        addBusiness,
        yearlyRevenue,
        customerSatisfaction,
        employeeCount,
        websiteTraffic,
        yearlyRevenueErrMsg,
        employeeCountErrMsg,
        customerSatisfactionErrMsg,
        websiteTrafficErrMsg,
        contactInfoErrMsg,
        inputClass,
        parseNumber,
        formatPhoneNumber,
        unformatPhoneNumber,
        formatBooleanValue
      };
    }
  }
</script>

<style scoped>
  .suggestion-item {
    padding: 8px 12px;
    cursor: pointer;
  }
  
  .suggestion-item:hover {
    background-color: #f0f0f0;
  }

  input {
    color: #000000;
  }
  input::placeholder {
    color: #aaa;
  }

  .selected-text {
    color: black; /* Apply black color for selected text */
  }
</style>