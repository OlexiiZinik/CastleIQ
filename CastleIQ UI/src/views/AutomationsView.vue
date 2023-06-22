<template>
    <div class="d-flex mt-5 mb-3 ">
        <h1 class="">Автоматизації</h1>
        <!-- <a href="#" class="btn btn-primary ms-auto my-auto">Додати автоматизацію</a>
        <a href="#" class="btn btn-primary ms-auto my-auto">Додати автоматизацію</a> -->
        <!-- <button type="button" class="btn btn-primary ms-auto my-auto">
            Додати автоматизацію
        </button> -->
        <!-- <a href="#" class="btn btn-primary ms-auto my-auto">Додати пристрій</a> -->
        <button type="button" class="btn btn-primary ms-auto my-auto" data-bs-toggle="modal"
            data-bs-target="#addAutomationModal">
            Додати автоматизацію
        </button>

        <!-- Modal -->
        <div class="modal fade" id="addAutomationModal" tabindex="-1" aria-labelledby="addAutomationModalLabel"
            aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h1 class="modal-title fs-5" id="addAutomationModal">Додавання автоматизації</h1>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <form class="" @submit.prevent="addAutomation">
                        <div class="modal-body">
                            <label class="form-label" for="name">Назва автоматизації</label>
                            <input type="text" id="name" class="form-control mb-2" placeholder="Назва" v-model="name" />

                            <label class="form-label" for="description">Опис автоматизації</label>
                            <input type="text" id="description" class="form-control mb-2" placeholder="Опис"
                                v-model="description" />

                            <label class="form-label" for="subscribed_on">По події</label>
                            <input type="text" id="subscribed_on" class="form-control mb-2" placeholder="По події"
                                v-model="subscribed_on" />

                            <div class="form-floating">
                                <textarea class="form-control" placeholder="Код автоматизації" id="code"
                                    style="height: 100px" v-model="code"></textarea>
                                <label for="code">Код автоматизації</label>
                            </div>
                            <!-- <label class="form-label" for="protocol">Протокол</label>
                            <select class="form-select mb-2" id="protocol" aria-label="protocol" v-model="protocol">
                                <option selected value="http">HTTP</option>
                                <option value="https">HTTPS</option>
                            </select>
                            <label class="form-label" for="ip">IP пристрою</label>
                            <input type="text" id="ip" class="form-control mb-2" placeholder="IP пристрою" v-model="ip" />
                            <label class="form-label" for="port">Порт</label>
                            <input type="number" id="port" class="form-control mb-2" placeholder="Порт" v-model="port" />
                            <label class="form-label" for="webhookPath">Шлях до вебхуку</label>
                            <input type="text" id="webhookPath" class="form-control mb-2" placeholder="Шлях до вебхуку"
                                v-model="webhookPath" />
                            <label class="form-label" for="room">Кімната</label>
                            <input type="text" id="room" class="form-control mb-2" placeholder="Кімната" v-model="room" /> -->
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Відмінити</button>
                            <button type="submit" class="btn btn-primary" data-bs-dismiss="modal">Додати</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
        <button type="button" class="btn btn-secondary ms-2 my-auto"
            v-on:click="this.$store.dispatch('automations/updateAutomations')">
            Оновити
        </button>
    </div>
    <div class="row">
        <div v-for="automation in this.$store.state.automations.automations" class="card  p-0 mb-4">
            <div class="card-header d-flex">
                <h5 class="card-title my-auto">{{ automation.name }}</h5>
                <div class="form-check form-switch ms-auto">
                    <input class="form-check-input" type="checkbox" checked role="switch">
                </div>
            </div>
            <div class="card-body">
                <h5 class="card-title">{{ automation.description }}</h5>
                <h6 class="card-title">При {{ automation.subscribed_on }} -></h6>
                <p class="card-text">{{ automation.code }}</p>
                <a href="#" class="btn btn-primary">Редагувати</a>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            name: "",
            description: "",
            subscribed_on: "",
            code: ""
        }
    },

    methods: {
        addAutomation(event) {
            this.$store.dispatch("automations/addAutomation", {
                event_type: "RequestEvent",
                event_name: "CreateAutomation",
                automation:{
                    name: this.name,
                    description: this.description,
                    subscribed_on: this.subscribed_on,
                    code: this.code,
                },
            })
        }
    },
    components: {
    },
    async mounted() {
        this.$store.dispatch("automations/getAllAutomations")
    }
}
</script>