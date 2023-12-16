<template>
    <div class="space-y-6">
      <p v-if="formErrMsg" class="text-sm text-red-600 mt-1">{{ formErrMsg }}</p>
      <button @click="addBusiness" class="w-full rounded-md bg-indigo-600 px-3 py-2 text-white shadow-sm hover:bg-indigo-500">Add Business</button>
    </div>
  </template>
    
<script>
import axios from 'axios';
import { inject, nextTick, ref } from 'vue';
import EventBus from '../../../eventBus';
  
    export default {
      setup() {
        const address = inject('address');
        const businessName = inject('businessName');
        const contactInfo = inject('contactInfo');
        const hasAvailableResourcesBoolean = inject('hasAvailableResourcesBoolean');
        const organizationType = inject('organizationType');
        const resourcesAvailable = inject('resourcesAvailable');
        const addressErrMsg = inject('addressErrMsg');
        const zipcodeErrMsg = inject('zipcodeErrMsg');
        const formErrMsg = ref('');
  
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
            has_available_resources: hasAvailableResourcesBoolean.value === 'true',
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

        const scrollToField = async (fieldName) => {
          await nextTick();
          const element = document.getElementById(fieldName);
          if (element) {
            element.scrollIntoView({ behavior: 'smooth', block: 'center' });
          }
        };
  
        
        return {
            businessName,
            address,
            organizationType,
            resourcesAvailable,
            hasAvailableResourcesBoolean,
            contactInfo,
            EventBus,
            addBusiness,
            formErrMsg,
            zipcodeErrMsg,
            addressErrMsg,
        };
      }
    };
  </script>
  
<style></style>