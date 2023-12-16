<template>
    <TransitionRoot as="template" :show="isDialogOpen">
        <Dialog as="div" class="fixed inset-0 z-10 overflow-y-auto" @close="closeModal">
            <div class="flex items-end justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
                <TransitionChild as="template" enter="ease-out duration-300" enter-from="opacity-0" enter-to="opacity-100" leave="ease-in duration-200" leave-from="opacity-100" leave-to="opacity-0">
                    <DialogOverlay class="fixed inset-0 transition-opacity bg-black bg-opacity-50" />
                </TransitionChild>

                <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
                <TransitionChild as="template" enter="ease-out duration-300" enter-from="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95" enter-to="opacity-100 translate-y-0 sm:scale-100" leave="ease-in duration-200" leave-from="opacity-100 translate-y-0 sm:scale-100" leave-to="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95">
                    <DialogPanel :class="['inline-block align-bottom bg-white rounded-lg overflow-hidden shadow-xl transform transition-all sm:align-middle', isExpanded ? 'fixed inset-0 z-50 w-full h-full max-w-none p-0' : 'sm:my-8 sm:max-w-lg sm:w-full sm:p-6']">
                        <div class="absolute top-0 right-0 p-6 cursor-pointer hover-effect icon-container" @click="toggleModalSize">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 3.75v4.5m0-4.5h4.5m-4.5 0L9 9M3.75 20.25v-4.5m0 4.5h4.5m-4.5 0L9 15M20.25 3.75h-4.5m4.5 0v4.5m0-4.5L15 9m5.25 11.25h-4.5m4.5 0v-4.5m0 4.5L15 15" />
                            </svg>
                        </div>
                        <iframe :src="mapEmbedUrl" width="100%" :height="isExpanded ? '100%' : '500'" frameborder="0" allowfullscreen></iframe>
                    </DialogPanel>
                </TransitionChild>
            </div>
        </Dialog>
    </TransitionRoot>
</template>

<script>
import { Dialog, DialogOverlay, DialogPanel, TransitionChild, TransitionRoot } from '@headlessui/vue';
import { inject } from 'vue';

export default {
  components: {
    Dialog,
    DialogPanel,
    DialogOverlay,
    TransitionRoot,
    TransitionChild,
  },
  setup() {
    const isDialogOpen = inject('isDialogOpen');
    const mapEmbedUrl = inject('mapEmbedUrl');
    const isExpanded = inject('isExpanded');
    const formattedAddress = inject('formattedAddress');
    const openModal = inject('openModal');

    const closeModal = () => {
        isDialogOpen.value = false;
    }

    const toggleModalSize = () => {
        isExpanded.value = !isExpanded.value;
    }

    return {
        isDialogOpen,
        mapEmbedUrl,
        isExpanded,
        openModal,
        closeModal,
        toggleModalSize,
        formattedAddress
    };
  }
};
</script>

<style scoped>
.icon-container {
    position: absolute;
    top: 10px;
    right: 10px;
    background-color: white;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 20;
    padding: 5px;
}

.icon-container:hover {
    transform: scale(1.1);
    transition: transform 0.3s ease-in-out;
}

.icon-container svg {
    fill: black;
    width: 30px;
    height: 30px;
    z-index: 30;
}

svg {
    color: black;
}
</style>