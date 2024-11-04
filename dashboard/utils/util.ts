import { resolve } from "chart.js/helpers"

export const sleep = (ms:number)=>{
    return new Promise(resolve => setTimeout(resolve, ms));
}

 
export const getWeeksInMonth:any = (year:number, month:number)=> {
    // Month is 0-indexed in JavaScript (0 = January, 11 = December)
    const firstDay = new Date(year, month, 1);  // First day of the month
    const lastDay = new Date(year, month + 1, 0);  // Last day of the month
    
    // Get the day of the week for the first and last day (0 = Sunday, 6 = Saturday)
    const firstDayOfWeek = firstDay.getDay();
    const lastDate = lastDay.getDate();
    
    // Calculate the number of weeks
    const weeks = Math.ceil((firstDayOfWeek + lastDate) / 7)
    let data = []
    if (weeks === 5){
        data = [{'week': 'WEEK 1', 'studentsPresent': 0, 'days': 
            [{'day': 'MONDAY', 'studentsPresent': 0}, {'day': 'TUESDAY', 'studentsPresent': 0}, {'day': 'WEDNESDAY', 'studentsPresent': 0}, {'day': 'THURSDAY', 'studentsPresent': 0}, {'day': 'FRIDAY', 'studentsPresent': 0}]
        },
        {'week': 'WEEK 2', 'studentsPresent': 0, 'days': 
            [{'day': 'MONDAY', 'studentsPresent': 0}, {'day': 'TUESDAY', 'studentsPresent': 0}, {'day': 'WEDNESDAY', 'studentsPresent': 0}, {'day': 'THURSDAY', 'studentsPresent': 0}, {'day': 'FRIDAY', 'studentsPresent': 0}]
        },
        {'week': 'WEEK 3', 'studentsPresent': 0, 'days': 
            [{'day': 'MONDAY', 'studentsPresent': 0}, {'day': 'TUESDAY', 'studentsPresent': 0}, {'day': 'WEDNESDAY', 'studentsPresent': 0}, {'day': 'THURSDAY', 'studentsPresent': 0}, {'day': 'FRIDAY', 'studentsPresent': 0}]
        },
        {'week': 'WEEK 4', 'studentsPresent': 0, 'days': 
            [{'day': 'MONDAY', 'studentsPresent': 0}, {'day': 'TUESDAY', 'studentsPresent': 0}, {'day': 'WEDNESDAY', 'studentsPresent': 0}, {'day': 'THURSDAY', 'studentsPresent': 0}, {'day': 'FRIDAY', 'studentsPresent': 0}]
        },
        {'week': 'WEEK 5', 'studentsPresent': 0, 'days': 
            [{'day': 'MONDAY', 'studentsPresent': 0}, {'day': 'TUESDAY', 'studentsPresent': 0}, {'day': 'WEDNESDAY', 'studentsPresent': 0}, {'day': 'THURSDAY', 'studentsPresent': 0}, {'day': 'FRIDAY', 'studentsPresent': 0}]
        }
        ]
    }else{
        data = [{'week': 'WEEK 1', 'studentsPresent': 0, 'days': 
            [{'day': 'MONDAY', 'studentsPresent': 0}, {'day': 'TUESDAY', 'studentsPresent': 0}, {'day': 'WEDNESDAY', 'studentsPresent': 0}, {'day': 'THURSDAY', 'studentsPresent': 0}, {'day': 'FRIDAY', 'studentsPresent': 0}]
        },
        {'week': 'WEEK 2', 'studentsPresent': 0, 'days': 
            [{'day': 'MONDAY', 'studentsPresent': 0}, {'day': 'TUESDAY', 'studentsPresent': 0}, {'day': 'WEDNESDAY', 'studentsPresent': 0}, {'day': 'THURSDAY', 'studentsPresent': 0}, {'day': 'FRIDAY', 'studentsPresent': 0}]
        },
        {'week': 'WEEK 3', 'studentsPresent': 0, 'days': 
            [{'day': 'MONDAY', 'studentsPresent': 0}, {'day': 'TUESDAY', 'studentsPresent': 0}, {'day': 'WEDNESDAY', 'studentsPresent': 0}, {'day': 'THURSDAY', 'studentsPresent': 0}, {'day': 'FRIDAY', 'studentsPresent': 0}]
        },
        {'week': 'WEEK 4', 'studentsPresent': 0, 'days': 
            [{'day': 'MONDAY', 'studentsPresent': 0}, {'day': 'TUESDAY', 'studentsPresent': 0}, {'day': 'WEDNESDAY', 'studentsPresent': 0}, {'day': 'THURSDAY', 'studentsPresent': 0}, {'day': 'FRIDAY', 'studentsPresent': 0}]
        },
        ]
        
    }
    return data;
};

export const getWeekNumberInMonth = (date:any)=> {
    // Ensure the input is a valid Date object
    if (!(date instanceof Date)) {
      throw new Error('Invalid date');
    }
  
    // Get the day of the month (1-31)
    const day = date.getDate();
  
    // Calculate the week number
    const weekNumber = Math.ceil(day / 7);
  
    return weekNumber;
  }

  // Function to generate attendance data for each month in the academic year
export const getAttendanceData = (academicStartDate:any, academicEndDate:any)=> {
    const startMonth = academicStartDate.getMonth();  // Start month index (0-based)
    const startYear = academicStartDate.getFullYear();  // Start year
    const endMonth = academicEndDate.getMonth();  // End month index (0-based)
    const endYear = academicEndDate.getFullYear();  // End year
    
    const attendances = [];
    let currentYear = startYear;
    let currentMonth = startMonth;
    
    // Loop through the months from the start date to the end date
    while (currentYear < endYear || (currentYear === endYear && currentMonth <= endMonth)) {
      // Get the month name (optional)
      const monthName = new Date(currentYear, currentMonth).toLocaleString('en-US', { month: 'long' }).toUpperCase();
      
      // Push attendance data for the current month
      attendances.push({
        month: monthName,
        studentsPresent: 0,
        weeks: getWeeksInMonth(currentYear, currentMonth) // Use your existing function to get weeks
      });
      
      // Move to the next month
      currentMonth++;
      if (currentMonth > 11) {  // When December is reached, go to the next year
        currentMonth = 0;
        currentYear++;
      }
    }
    
    return attendances;
  }
  
export const getGradeColor = (grade:string)=>{
    const gradeColors = [
        {'grade': 'A1', 'color': '#006400'},  // Deep Green (Excellent)
        {'grade': 'B2', 'color': '#228B22'},  // Dark Green (Very Good)
        {'grade': 'B3', 'color': '#3CB371'},  // Medium Sea Green (Good)
        {'grade': 'C4', 'color': '#2E8B57'},  // Sea Green (Credit)
        {'grade': 'C5', 'color': '#00FA9A'},  // Medium Spring Green (Credit)
        {'grade': 'C6', 'color': '#90EE90'},  // Light Green (Credit)
        {'grade': 'D7', 'color': '#98FB98'},  // Pale Green (Pass)
        {'grade': 'E8', 'color': '#F5FFFA'},  // Mint Cream (Pass)
        {'grade': 'F9', 'color': '#F0FFF0'}   // Honeydew (Fail)
    ];
    const colorItem = gradeColors.find(item => item['grade'] === grade)
    if (colorItem){
        return colorItem['color']
    }else{
        return 'black'
    }
}
