<!-- Main entry screen containing the splash logo as well as the various sections of the website. -->

<template>
  <header class="sticky top-0 inset-x-0 -mt-12 flex flex-wrap sm:justify-start sm:flex-nowrap z-40 bg-white text-sm dark:bg-gray-800">
    <nav class="max-w-full w-full mx-auto px-4 sm:flex sm:items-center sm:justify-between" aria-label="Global">
      <div class="flex items-center justify-between">
        <a class="flex-none" href="#">
          <img class="w-10 h-auto rounded-full" src="@/assets/cropped_final_logo.png" alt="Logo">
        </a>
        <div class="sm:hidden">
          <button type="button" class="hs-collapse-toggle p-2 inline-flex justify-center items-center gap-x-2 rounded-lg border border-gray-200 bg-white text-gray-800 shadow-sm hover:bg-gray-50 disabled:opacity-50 disabled:pointer-events-none dark:bg-transparent dark:border-gray-700 dark:text-white dark:hover:bg-white/10 dark:focus:outline-none dark:focus:ring-1 dark:focus:ring-gray-600" data-hs-collapse="#navbar-image-1" aria-controls="navbar-image-1" aria-label="Toggle navigation">
            <svg class="hs-collapse-open:hidden flex-shrink-0 w-4 h-4" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" x2="21" y1="6" y2="6"/><line x1="3" x2="21" y1="12" y2="12"/><line x1="3" x2="21" y1="18" y2="18"/></svg>
            <svg class="hs-collapse-open:block hidden flex-shrink-0 w-4 h-4" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
          </button>
        </div>
      </div>
      <div id="navbar-image-1" class="hs-collapse hidden overflow-hidden transition-all duration-300 basis-full grow sm:block">
        <div data-hs-scrollspy="#scrollspy-1" class="flex flex-col gap-5 sm:flex-row sm:items-center sm:justify-end sm:mt-0 sm:ps-5">
          <a :class="{ 'text-indigo-600': currentSection === 'home' }" @click.prevent="navigateToSection('home')">Home</a>
          <a :class="{ 'text-indigo-600': currentSection === 'about' }" @click.prevent="navigateToSection('about')">About</a>
          <a :class="{ 'text-indigo-600': currentSection === 'work' }" @click.prevent="navigateToSection('work')">Work</a>
          <a :class="{ 'text-indigo-600': currentSection === 'blog' }" @click.prevent="navigateToSection('blog')">Blog</a>
          <button
            @click="openModal"
            class="mt-0.5 flex justify-center items-center rounded-lg px-3.5 py-0.5 overflow-hidden relative group cursor-pointer border-2 font-medium border-indigo-600 text-indigo-600"
          >
            <span class="absolute w-64 h-0 transition-all duration-300 origin-center rotate-45 -translate-x-20 bg-indigo-600 top-1/2 group-hover:h-64 group-hover:-translate-y-32 ease"></span>
            <span class="relative transition duration-300 group-hover:text-white ease">Log In</span>
          </button>
          <DarkModeSwitch class="mt-11"></DarkModeSwitch>
        </div>
      </div>
    </nav>
  </header>

  <div id="home" class="section flex flex-col justify-center items-center relative h-screen space-y-4">
    <div class="opacity-0 animate-fadeIn animation-delay-500">
      <h1 class="text-7xl font-mono mb-4">Welcome</h1>
    </div>

    <div class="opacity-0 animate-fadeIn animation-delay-1000">
      <p class="text-lg font-mono mb-4">The database of the future.</p>
    </div>

    <TransitionRoot :show="isOpen" as="template">
      <Dialog as="div" @close="closeModal" class="fixed inset-0 overflow-y-auto z-50">
        <div class="flex min-h-full items-center justify-center p-4 text-center">
          <TransitionChild
            as="template"
            enter="duration-300 ease-out"
            enter-from="opacity-0 scale-95"
            enter-to="opacity-100 scale-100"
            leave="duration-200 ease-in"
            leave-from="opacity-100 scale-100"
            leave-to="opacity-0 scale-95"
          >
            <DialogPanel class="w-full md:w-[800px] transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all z-50 dark:bg-gray-800">
              <LoginComponent />
            </DialogPanel>
          </TransitionChild>
        </div>
      </Dialog>
    </TransitionRoot>
  </div>
  <div id="about" class="mt-12 section relative h-screen overflow-hidden">
    <h3 class="text-3xl font-semibold text-center">About Us</h3>
    <p class="text-lg text-center mt-10">We are a small team working on the next-generation business solution. Updates coming soon.</p>
  </div>
  
  <div id="work" class="section relative h-screen">
    <h3 class="text-3xl font-semibold text-center">Our Work</h3>
    <p class="text-lg text-center mt-10">Our team has made several solutions in the past.</p>
  </div>
  
  <div id="blog" class="section relative h-screen">
    <h3 class="text-3xl font-semibold text-center">Blog</h3>
    <p class="text-lg text-center mt-10">Follow our newest ventures here.</p>
  </div>
</template>

<script>
import { Dialog, DialogPanel, TransitionChild, TransitionRoot } from '@headlessui/vue';
import { nextTick, onMounted, onUnmounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import LoginComponent from '../Forms/LoginComponent.vue';
import DarkModeSwitch from '../UI Enhancements/DarkModeSwitch.vue';

export default {
  components: {
    LoginComponent,
    TransitionRoot,
    TransitionChild,
    Dialog,
    DialogPanel,
    DarkModeSwitch
  },
  setup() {
    const router = useRouter();
    const isOpen = ref(false);
    const currentSection = ref(null);
    const sectionsRefs = ref([]);

    const openModal = () => {
      isOpen.value = true;
    };

    const closeModal = () => {
      isOpen.value = false;
    };

    const redirectToLogin = () => {
      router.push({ name: 'LoginPage' });
    };

    const onScroll = () => {
      let foundSection = null;
      sectionsRefs.value.forEach(section => {
        const rect = section.getBoundingClientRect();
        if (rect.top >= 0 && rect.top <= window.innerHeight / 2) {
          foundSection = section.id;
        }
      });
      currentSection.value = foundSection;
    };

    const adjustScroll = () => {
        const headerHeight = document.querySelector('.sticky').offsetHeight;
        window.scrollBy(0, -headerHeight);
    };

    const navigateToSection = (sectionId) => {
      nextTick(() => {
        const section = document.getElementById(sectionId);
        if (section) {
          const headerHeight = document.querySelector('.sticky') ? document.querySelector('.sticky').offsetHeight : 0;
          const sectionTop = window.scrollY + section.getBoundingClientRect().top - headerHeight;
          
          window.scrollTo({
            top: sectionTop,
            behavior: "smooth"
          });

          currentSection.value = sectionId;
        }
      });
    };


    onMounted(() => {
      sectionsRefs.value = document.querySelectorAll('.section');
      window.addEventListener('scroll', onScroll);
      onScroll();
    });

    onUnmounted(() => {
      window.removeEventListener('scroll', onScroll);
    });
    
    return {
      redirectToLogin,
      isOpen,
      openModal,
      closeModal,
      onScroll,
      currentSection,
      sectionsRefs,
      adjustScroll,
      navigateToSection
    };
  }
}
</script>

<style scoped>
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.animate-fadeIn {
  animation-name: fadeIn;
  animation-duration: 1.5s;
  animation-fill-mode: forwards;
}

.animation-delay-500 {
  animation-delay: 0.75s;
}

.animation-delay-1000 {
  animation-delay: 1.5s;
}

.animation-delay-1500 {
  animation-delay: 2.25s;
}
</style>