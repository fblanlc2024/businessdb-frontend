<template>
  <div class="space-y-6">
    <h2 class="text-2xl font-bold text-gray-900 text-center mt-5">Add New Business Client</h2>

    <!-- Business Name -->
    <div>
      <label for="businessName" class="block text-sm font-medium text-gray-900">Business Name</label>
      <input id="businessName" v-model="businessName" required placeholder="Enter business name" class="mt-2 block w-full rounded-md border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
    </div>

    <div>
      <label for="addressLookup" class="block text-sm font-medium text-gray-900">Address Lookup</label>
      <input id="addressLookup" v-model="addressLookupQuery" placeholder="Start typing an address..." class="mt-2 block w-full rounded-md border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
      <div v-if="addressSuggestions.length" class="mt-2 bg-white rounded-md shadow-lg">
        <ul>
          <li v-for="suggestion in addressSuggestions" :key="suggestion.fsq_id" @click="selectAddressSuggestion(suggestion)" class="suggestion-item">
            {{ suggestion.name }} - {{ suggestion.location.formatted_address }}
          </li>
        </ul>
      </div>
    </div>

    <!-- Address Fields -->
    <div>
      <label class="block text-sm font-medium text-gray-900">Address</label>
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 8px;">
        <div>
          <input id="address" v-model="address.number" :class="inputClass(addressErrMsg)" placeholder="Number" />
          <p v-if="addressErrMsg" class="text-red-500 text-xs">{{ addressErrMsg }}</p>
        </div>
        <div>
          <input v-model="address.street" placeholder="Street" class="block w-full rounded-md border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
        </div>
        <div>
          <input v-model="address.city" placeholder="City" class="block w-full rounded-md border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
        </div>
        <div>
          <input 
            id="zipcode"
            v-model="address.zipcode" 
            :class="inputClass(zipcodeErrMsg)" 
            placeholder="Zipcode" 
          />
          <p v-if="zipcodeErrMsg" class="text-red-500 text-xs">{{ zipcodeErrMsg }}</p>
        </div>
        <div>
          <select v-model="address.state" class="block w-full rounded-md border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
            <option value="" disabled selected>Select State</option>
            <option v-for="state in states" :key="state" :value="state">{{ state }}</option>
          </select>
        </div>

        <div>
          <select v-model="address.country" class="block w-full rounded-md border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
            <option value="" disabled selected>Select Country</option>
            <option v-for="country in countries" :key="country" :value="country">{{ country }}</option>
          </select>
        </div>
      </div>
    </div>

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
      <select id="hasAvailableResources" v-model="hasAvailableResources" required class="mt-2 block w-full rounded-md border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
        <option value="" disabled selected hidden>Select option</option>
        <option value="true">Yes</option>
        <option value="false">No</option>
      </select>
    </div>

    <!-- Contact Info -->
    <div>
      <label for="contactInfo" class="block text-sm font-medium text-gray-900">Contact Info</label>
      <input id="contactInfo" v-model="contactInfo" required placeholder="Enter contact info" class="mt-2 block w-full rounded-md border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
    </div>
    
    <p v-if="formErrMsg" class="text-sm text-red-600 mt-1">{{ formErrMsg }}</p>
    <button @click="addBusiness" class="w-full rounded-md bg-indigo-600 px-3 py-2 text-white shadow-sm hover:bg-indigo-500">Add Business</button>
  </div>
</template>
  
<script>
import axios from 'axios';
import { computed, nextTick, ref, watch } from 'vue';
import EventBus from '../eventBus';

  export default {
    setup() {
      const businessName = ref('');
      const address = ref({
        number: '',
        street: '',
        city: '',
        state: '',
        zipcode: '',
        country: ''
      });
      
      const organizationType = ref('');
      const resourcesAvailable = ref('');
      const hasAvailableResources = ref('');
      const contactInfo = ref('');
      const addressLookupQuery = ref('');
      const addressSuggestions = ref([]);
      const states = ref(['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']);
      const countries = ref(['US', 'CA', 'MX']);
      const formErrMsg = ref('');
      const zipcodeErrMsg = ref('');
      const addressErrMsg = ref('');
      const optionsBool = ref({
        '': '',
        'true': true,
        'false': false
      })

      watch(addressLookupQuery, async (newQuery) => {
        if (newQuery && newQuery.length > 2) {
          try {
            const response = await axios.get(`https://localhost:5000/autocomplete?query=${newQuery}`);
            addressSuggestions.value = response.data.results;
          } catch (error) {
            console.error('Error fetching address suggestions:', error);
          }
        } else {
          addressSuggestions.value = [];
        }
      });

      const hasAvailableResourcesBoolean = computed({
        get: () => hasAvailableResources.value === 'true',
        set: (newValue) => {
          hasAvailableResources.value = newValue ? 'true' : 'false';
        }
      });

      const addBusiness = async () => {
        console.log('Sending hasAvailableResources:', hasAvailableResourcesBoolean.value);
        const businessData = {
          business_name: businessName.value, // Ensure key matches backend
          address: {
            number: address.value.number,
            street: address.value.street,
            city: address.value.city,
            state: address.value.state,
            zipcode: address.value.zipcode,
            country: address.value.country
          },
          organization_type: organizationType.value,
          resources_available: resourcesAvailable.value,
          has_available_resources: hasAvailableResourcesBoolean.value,
          contact_info: contactInfo.value
        };
  
        try {
          const response = await axios.post('https://localhost:5000/add_business', businessData);
          console.log(response.data);
          EventBus.emit('business-added', response.data);
          EventBus.emit('close-modal');
        } catch (error) {
          if (error.response && error.response.data && error.response.data.error) {
            let errorMsg = error.response.data.error;
            errorMsg = errorMsg.replace(/['"]+/g, '').replace(/&quot;/g, '');

            addressErrMsg.value = '';
            zipcodeErrMsg.value = '';
            
            if (errorMsg.includes('zipcode')) {
              zipcodeErrMsg.value = errorMsg;
              scrollToField('zipcode');
            } else if (errorMsg.includes('integer')) {
              addressErrMsg.value = errorMsg;
              scrollToField('address');
            } else {
              formErrMsg.value = errorMsg;
            }
          } else {
            formErrMsg.value = 'Network error. Please try again later.';
          }
          console.error('Error adding business:', error);
        }
      };

      const inputClass = (errorMsg) => {
        return [
          'block w-full rounded-md border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
          errorMsg ? 'border-red-500' : ''
        ];
      };

      const scrollToField = async (fieldName) => {
        await nextTick();
        const element = document.getElementById(fieldName);
        if (element) {
          element.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
      };

      const fetchAddressSuggestions = async () => {
        if (addressLookupQuery.value.length > 2) {
          try {
            const response = await axios.get(`https://localhost:5000/autocomplete?query=${addressLookupQuery.value}`);
            addressSuggestions.value = response.data;
          } catch (error) {
            console.error('Error fetching address suggestions:', error);
          }
        }
      };

      const selectAddressSuggestion = (suggestion) => {
        const { location } = suggestion;
        address.value = {
          number: location.address.split(' ')[0],
          street: location.address.split(' ').slice(1).join(' '),
          city: location.locality,
          state: location.region,
          zipcode: location.postcode,
          country: location.country
        };

        addressSuggestions.value = [];
      };

      return {
        businessName,
        address,
        organizationType,
        resourcesAvailable,
        hasAvailableResources,
        contactInfo,
        EventBus,
        addBusiness,
        addressLookupQuery,
        addressSuggestions,
        fetchAddressSuggestions,
        selectAddressSuggestion,
        states,
        countries,
        formErrMsg,
        zipcodeErrMsg,
        addressErrMsg,
        inputClass,
        optionsBool
      };
    }
  };
</script>

<style>
.suggestion-item {
  padding: 8px 12px;
  cursor: pointer;
}

.suggestion-item:hover {
  background-color: #f0f0f0;
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  border: 0;
}

</style>