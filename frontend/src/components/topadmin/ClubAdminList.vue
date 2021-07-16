<template>
  <v-container>
    <h1>Club administrator list</h1>
    <br />
    <v-layout v-if="clubAdmins.length > 0" row wrap>
      <v-flex v-for="admin in clubAdmins" :key="admin.name" xs12 sm6 md4 lg3>
        <v-hover>
          <v-card
            slot-scope="{ hover }"
            :class="`elevation-${hover ? 12 : 2}`"
            class="text-xs-center ma-3"
          >
            <v-responsive class="pt-4">
              <v-layout align-center justify-center row fill-height>
                <v-avatar size="80px">
                  <img :src="admin.image_url" />
                </v-avatar>
              </v-layout>
            </v-responsive>
            <v-card-text>
              <div class="grey--text">{{ admin.email }}</div>
            </v-card-text>
            <v-card-actions>
              <v-layout column>
                <v-btn text color="grey" @click="resetClubAdminPassword(admin)">
                  <v-icon small left>replay</v-icon>
                  <span>Reset password</span>
                </v-btn>
                <v-btn text color="grey" @click="showDeleteDialog(admin)">
                  <v-icon small left>delete_sweep</v-icon>
                  <span>Delete club admin</span>
                </v-btn>
              </v-layout>
            </v-card-actions>
          </v-card>
        </v-hover>
      </v-flex>
    </v-layout>
    <v-layout v-else class="justify-center">
      <div>
        <p class="subheading">
          There are no club admins, once you add them you can find them here.
        </p>
      </div>
    </v-layout>
    <v-btn
      style="bottom:50px;"
      dark
      small
      absolute
      bottom
      right
      fab
      fixed
      @click="$router.push('/add-club-admin')"
    >
      <v-icon>add</v-icon>
    </v-btn>

    <v-dialog v-model="removeDialogActive" persistent max-width="290">
      <v-card>
        <div>
          <v-card-text>
            Are you sure you want to remove this club?<br />
            This action can not be reversed.
          </v-card-text>
          <v-card-actions>
            <v-btn text @click="cancelDelete()">Cancel</v-btn>
            <v-spacer></v-spacer>

            <v-btn text @click="deleteUser()">
              Ok
            </v-btn>
          </v-card-actions>
        </div>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ClubAdminList',
  data: function() {
    return {
      clubAdmins: [],
      selectedClubAdmin: {},
      removeDialogActive: false,
    }
  },
  computed: {
    currentClub() {
      return this.$store.getters.getSelectedClub
    },
  },
  watch: {
    currentClub() {
      this.getClubAdmins()
    },
  },
  mounted() {
    this.getClubAdmins()
  },
  methods: {
    getClubAdmins() {
      axios
        .get('/api/club/admin/all', {
          params: { club_id: this.$store.getters.getSelectedClub._id },
        })
        .then(res => {
          this.clubAdmins = res.data
        })
    },
    resetClubAdminPassword(clubAdmin) {
      axios.put('/api/club/admin/reset', null, {
        params: { user_id: clubAdmin._id },
      })
    },
    showDeleteDialog(clubAdmin) {
      this.selectedClubAdmin = clubAdmin
      this.removeDialogActive = true
    },
    cancelDelete() {
      this.selectedClubAdmin = null
      this.removeDialogActive = false
    },
    deleteUser() {
      axios
        .delete('/api/club/admin', {
          params: { user_id: this.selectedClubAdmin._id },
        })
        .then(() => {
          this.getClubAdmins()
        })
      this.removeDialogActive = false
    },
    addOnClick() {},
  },
}
</script>

<style scoped></style>
