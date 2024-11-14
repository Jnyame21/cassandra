// Interfaces
interface DayAttendance {
    day: string;
    studentsPresent: number;
}

interface WeekAttendance {
    week: string;
    studentsPresent: number;
    days: DayAttendance[];
}

interface AttendanceMonth {
    month: string;
    studentsPresent: number;
    weeks: WeekAttendance[];
}

// Functions

export const sleep = (ms: number): Promise<void> => {
    return new Promise(resolve => setTimeout(resolve, ms));
};

// download a file sent from django using django's FileRsponse 
export const downloadFile = (responseHeaders:any, responseData:any, defaultFileName:string) => {
    const url = window.URL.createObjectURL(new Blob([responseData]))
    const link = document.createElement('a')
    link.href = url
    let fileName = defaultFileName
    const contentDisposition = responseHeaders['content-disposition']
    if (contentDisposition){
        const match = contentDisposition.match(/filename="(.+)"/)
        if (match){
            fileName = match[1]
        }
    }
    link.setAttribute('download', fileName)
    document.body.appendChild(link)
    link.click()
    window.URL.revokeObjectURL(url)
    link.remove()
};

export const getWeeksInMonth = (year: number, month: number): WeekAttendance[] => {
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const firstDayOfWeek = firstDay.getDay();
    const lastDate = lastDay.getDate();
    const weeks = Math.ceil((lastDate + firstDayOfWeek) / 7);
    const weekData: WeekAttendance[] = [];
    let dayCount = 1
    for (let i = 0; i < weeks; i++) {
        const weekNumber = i + 1;
        const daysInWeek = []
        if (weekNumber === 1){
            for (let j = 0; j < (7-firstDayOfWeek); j++){
                const dayDate = new Date(year, month, dayCount)
                if (![0, 6].includes(dayDate.getDay())){
                    daysInWeek.push(`${dayDate.toLocaleString('default', {'weekday': 'short'}).toUpperCase()}(${dayDate.toLocaleString('default', {'month': 'short'}).toUpperCase()} ${dayCount})`)
                }
                dayCount++
            }
        }
        else{
            for (let j = 0; j < 7; j++){
                if (dayCount > lastDate) break;
                const dayDate = new Date(year, month, dayCount)
                if (![0, 6].includes(dayDate.getDay())){
                    daysInWeek.push(`${dayDate.toLocaleString('default', {'weekday': 'short'}).toUpperCase()}(${dayDate.toLocaleString('default', {'month': 'short'}).toUpperCase()} ${dayCount})`)
                }
                dayCount++
            }
        }
        weekData.push({
            week: `WEEK ${weekNumber}`,
            studentsPresent: 0,
            days: daysInWeek.map(day => ({
                day,
                studentsPresent: 0
            }))
        });
    }
    return weekData;
};

export const getWeekNumberInMonth = (date: Date): number => {
    if (!(date instanceof Date)) {
        throw new Error('Invalid date');
    }
    const day = date.getDate();
    const firstDayOfMonth = new Date(date.getFullYear(), date.getMonth(), 1).getDay()
    const weekNumber = Math.ceil((day + firstDayOfMonth) / 7);
    return weekNumber;
};

const gradeColorsMap: Map<string, string> = new Map([
    ['A1', '#006400'],  // Deep Green (Excellent)
    ['B2', '#228B22'],  // Dark Green (Very Good)
    ['B3', '#3CB371'],  // Medium Sea Green (Good)
    ['C4', '#2E8B57'],  // Sea Green (Credit)
    ['C5', '#00FA9A'],  // Medium Spring Green (Credit)
    ['C6', '#90EE90'],  // Light Green (Credit)
    ['D7', '#98FB98'],  // Pale Green (Pass)
    ['E8', '#F5FFFA'],  // Mint Cream (Pass)
    ['F9', '#F0FFF0']   // Honeydew (Fail)
]);

export const getGradeColor = (grade: string): string => {
    return gradeColorsMap.get(grade) || 'black';
};

export const getAttendanceData = (academicStartDate: Date, academicEndDate: Date): AttendanceMonth[] => {
    const startMonth = academicStartDate.getMonth();
    const startYear = academicStartDate.getFullYear();
    const endMonth = academicEndDate.getMonth();
    const endYear = academicEndDate.getFullYear();
    
    const attendances: AttendanceMonth[] = [];
    let currentYear = startYear;
    let currentMonth = startMonth;
    
    while (currentYear < endYear || (currentYear === endYear && currentMonth <= endMonth)) {
        const monthName = new Date(currentYear, currentMonth).toLocaleString('default', { month: 'long' }).toUpperCase();
        
        attendances.push({
            month: monthName,
            studentsPresent: 0,
            weeks: getWeeksInMonth(currentYear, currentMonth)
        });
        
        currentMonth++;
        if (currentMonth > 11) {
            currentMonth = 0;
            currentYear++;
        }
    }
    
    return attendances;
};
