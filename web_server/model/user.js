var mongoose = require('mongoose');

var Schema = mongoose.Schema;

// Create a user schema.
var userSchema = new Schema({
  email: { type: String, required: true, unique: true },
  password: { type: String, required: true },
  created_at: Date,
  updated_at: Date
});

// On every save, update the timestamp.
userSchema.pre('save', function(next) {
  var currentDate = new Date();
  
  // Change the updated_at field to current date
  this.updated_at = currentDate;

  // If created_at doesn't exist, add to that field.
  if (!this.created_at)
    this.created_at = currentDate;
  next();
});

// Map the scehma to database.
var User = mongoose.model('users', userSchema);

module.exports = User;