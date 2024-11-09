export default {
    template: `
    <div class="content row justify-content-center">
      <div class="col-12 col-md-6 text-center">
        <h3 class='p-3 m-3'>Student Performance Prediction</h3>
        <div class="form-group">
            <label for="rollNumber" class="p-2 m-2 d-block text-center">Select Student Roll Number</label>
            <select v-model="selectedRollNumber" class="form-control" id="rollNumber">
                <option disabled value="">Choose Roll Number</option>
                <option v-for="student in students" :key="student.id" :value="student.id">{{ student.id }}</option>
            </select>
        </div>
        <button class="btn btn-primary mb-2" @click="predictPerformance">Predict Performance</button>
       </div>
      <div v-if="result" class="results-table">
        <h4 class="bg-success text-white p-2">Prediction Results</h4>
        <table class="table table-bordered">
          <thead>
            <tr>
              <th>Student ID</th>
              <th>Task Completion (%)</th>
              <th>Coding Activity (Hours)</th>
              <th>Predicted Performance</th>
              <th>Support Recommendation</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>{{ result.studentId }}</td>
              <td>{{ result.taskCompletion }}</td>
              <td>{{ result.codingActivity }}</td>
              <td>{{ result.predictedPerformance }}</td>
              <td>{{ result.supportRecommendation }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    `,
      
    data() {
        return{
            selectedRollNumber: '',
            students: [
              { id: '21fx' },
              { id: '22fx' },
              { id: '23fx' }
            ],
            result: null
      }},
    
    methods: {
        predictPerformance() {
            // Uncomment the following line and replace with your backend URL
            // axios.get('YOUR_BACKEND_URL/students/' + this.selectedRollNumber)
            //   .then(response => {
            //     this.result = response.data;
            //   });
  
            // Using dummy data for now
            this.result = {
              studentId: this.selectedRollNumber,
              taskCompletion: '60%',
              codingActivity: '5 hours',
              predictedPerformance: 'Medium',
              supportRecommendation: 'Consider additional support'
            };
        }
      }
  }
  