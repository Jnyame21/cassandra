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

export const sleep = (ms: number): Promise<void> => {
    return new Promise(resolve => setTimeout(resolve, ms));
};

export const headRoles:string[] = ['head master', 'head mistress', 'head of academics', 'assistant head of academics', 'assistant head master', 'assistant head mistress']

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

interface CountriesData{
  name: string
  nationality: string
}    

export const countriesData:CountriesData[] = [
  { name: "Afghanistan", nationality: "Afghan" },
  { name: "Albania", nationality: "Albanian" },
  { name: "Algeria", nationality: "Algerian" },
  { name: "Andorra", nationality: "Andorran" },
  { name: "Angola", nationality: "Angolan" },
  { name: "Antigua and Barbuda", nationality: "Antiguan" },
  { name: "Argentina", nationality: "Argentine" },
  { name: "Armenia", nationality: "Armenian" },
  { name: "Australia", nationality: "Australian" },
  { name: "Austria", nationality: "Austrian" },
  { name: "Azerbaijan", nationality: "Azerbaijani" },
  { name: "Bahamas", nationality: "Bahamian" },
  { name: "Bahrain", nationality: "Bahraini" },
  { name: "Bangladesh", nationality: "Bangladeshi" },
  { name: "Barbados", nationality: "Barbadian" },
  { name: "Belarus", nationality: "Belarusian" },
  { name: "Belgium", nationality: "Belgian" },
  { name: "Belize", nationality: "Belizean" },
  { name: "Benin", nationality: "Beninese" },
  { name: "Bhutan", nationality: "Bhutanese" },
  { name: "Bolivia", nationality: "Bolivian" },
  { name: "Bosnia and Herzegovina", nationality: "Bosnian" },
  { name: "Botswana", nationality: "Botswanan" },
  { name: "Brazil", nationality: "Brazilian" },
  { name: "Brunei", nationality: "Bruneian" },
  { name: "Bulgaria", nationality: "Bulgarian" },
  { name: "Burkina Faso", nationality: "Burkinabe" },
  { name: "Burundi", nationality: "Burundian" },
  { name: "Cabo Verde", nationality: "Cabo Verdean" },
  { name: "Cambodia", nationality: "Cambodian" },
  { name: "Cameroon", nationality: "Cameroonian" },
  { name: "Canada", nationality: "Canadian" },
  { name: "Central African Republic", nationality: "Central African" },
  { name: "Chad", nationality: "Chadian" },
  { name: "Chile", nationality: "Chilean" },
  { name: "China", nationality: "Chinese" },
  { name: "Colombia", nationality: "Colombian" },
  { name: "Comoros", nationality: "Comorian" },
  { name: "Côte d'Ivoire", nationality: "Ivorian" },
  { name: "Croatia", nationality: "Croatian" },
  { name: "Cuba", nationality: "Cuban" },
  { name: "Cyprus", nationality: "Cypriot" },
  { name: "Czech Republic", nationality: "Czech" },
  { name: "Democratic Republic of the Congo", nationality: "Congolese" },
  { name: "Denmark", nationality: "Danish" },
  { name: "Djibouti", nationality: "Djiboutian" },
  { name: "Dominican Republic", nationality: "Dominican" },
  { name: "Ecuador", nationality: "Ecuadorian" },
  { name: "Egypt", nationality: "Egyptian" },
  { name: "El Salvador", nationality: "Salvadoran" },
  { name: "Equatorial Guinea", nationality: "Equatorial Guinean" },
  { name: "Eritrea", nationality: "Eritrean" },
  { name: "Estonia", nationality: "Estonian" },
  { name: "Eswatini", nationality: "Eswatini" },
  { name: "Ethiopia", nationality: "Ethiopian" },
  { name: "Fiji", nationality: "Fijian" },
  { name: "Finland", nationality: "Finnish" },
  { name: "France", nationality: "French" },
  { name: "Gabon", nationality: "Gabonese" },
  { name: "Gambia", nationality: "Gambian" },
  { name: "Georgia", nationality: "Georgian" },
  { name: "Germany", nationality: "German" },
  { name: "Ghana", nationality: "Ghanaian" },
  { name: "Greece", nationality: "Greek" },
  { name: "Grenada", nationality: "Grenadian" },
  { name: "Guatemala", nationality: "Guatemalan" },
  { name: "Guinea", nationality: "Guinean" },
  { name: "Guinea-Bissau", nationality: "Bissau-Guinean" },
  { name: "Guyana", nationality: "Guyanese" },
  { name: "Haiti", nationality: "Haitian" },
  { name: "Honduras", nationality: "Honduran" },
  { name: "Hungary", nationality: "Hungarian" },
  { name: "Iceland", nationality: "Icelandic" },
  { name: "India", nationality: "Indian" },
  { name: "Indonesia", nationality: "Indonesian" },
  { name: "Iran", nationality: "Iranian" },
  { name: "Iraq", nationality: "Iraqi" },
  { name: "Ireland", nationality: "Irish" },
  { name: "Israel", nationality: "Israeli" },
  { name: "Italy", nationality: "Italian" },
  { name: "Jamaica", nationality: "Jamaican" },
  { name: "Japan", nationality: "Japanese" },
  { name: "Jordan", nationality: "Jordanian" },
  { name: "Kazakhstan", nationality: "Kazakh" },
  { name: "Kenya", nationality: "Kenyan" },
  { name: "Kiribati", nationality: "Kiribati" },
  { name: "Kosovo", nationality: "Kosovar" },
  { name: "Kuwait", nationality: "Kuwaiti" },
  { name: "Kyrgyzstan", nationality: "Kyrgyz" },
  { name: "Laos", nationality: "Lao" },
  { name: "Latvia", nationality: "Latvian" },
  { name: "Lebanon", nationality: "Lebanese" },
  { name: "Lesotho", nationality: "Basotho" },
  { name: "Liberia", nationality: "Liberian" },
  { name: "Libya", nationality: "Libyan" },
  { name: "Liechtenstein", nationality: "Liechtensteiner" },
  { name: "Lithuania", nationality: "Lithuanian" },
  { name: "Luxembourg", nationality: "Luxembourger" },
  { name: "Madagascar", nationality: "Malagasy" },
  { name: "Malawi", nationality: "Malawian" },
  { name: "Malaysia", nationality: "Malaysian" },
  { name: "Maldives", nationality: "Maldivian" },
  { name: "Mali", nationality: "Malian" },
  { name: "Malta", nationality: "Maltese" },
  { name: "Marshall Islands", nationality: "Marshallese" },
  { name: "Mauritania", nationality: "Mauritanian" },
  { name: "Mauritius", nationality: "Mauritian" },
  { name: "Mexico", nationality: "Mexican" },
  { name: "Micronesia", nationality: "Micronesian" },
  { name: "Moldova", nationality: "Moldovan" },
  { name: "Monaco", nationality: "Monegasque" },
  { name: "Mongolia", nationality: "Mongolian" },
  { name: "Montenegro", nationality: "Montenegrin" },
  { name: "Morocco", nationality: "Moroccan" },
  { name: "Mozambique", nationality: "Mozambican" },
  { name: "Namibia", nationality: "Namibian" },
  { name: "Nauru", nationality: "Nauruan" },
  { name: "Nepal", nationality: "Nepali" },
  { name: "Netherlands", nationality: "Dutch" },
  { name: "New Zealand", nationality: "New Zealander" },
  { name: "Nicaragua", nationality: "Nicaraguan" },
  { name: "Niger", nationality: "Nigerien" },
  { name: "Nigeria", nationality: "Nigerian" },
  { name: "North Macedonia", nationality: "North Macedonian" },
  { name: "Norway", nationality: "Norwegian" },
  { name: "Russia", nationality: "Russian" },
  { name: "South Africa", nationality: "South African" },
  { name: "South Korea", nationality: "Korean" },
  { name: "United Kingdom", nationality: "British" },
  { name: "United States", nationality: "American" }
]

export const ghanaRegions:string[] = [
  'Ashanti', 
  'Ahafo', 
  'Bono', 
  'Bono East', 
  'Central', 
  'Eastern', 
  'Greater Accra', 
  'Northern', 
  'North East', 
  'Oti', 
  'Savannah', 
  'Upper East', 
  'Upper West', 
  'Volta', 
  'Western', 
  'Western North'
]

export const genderOptions = [
  { 'label': 'MALE', 'value': 'male' },
  { 'label': 'FEMALE', 'value': 'female' },
]

export const uploadTypeOptions = [
  { 'label': 'USE AN EXCEL FILE', 'value': 'file' },
  { 'label': 'INPUT DATA HERE', 'value': 'noFile' },
]

export const titleOptions = ['Mr', 'Miss', 'Mrs', 'Dr', 'Prof', 'Rev', 'Sir', 'Hon', 'Madam', 'Pastor', 'Imam', 'Bishop', 'Archbishop']

export const religionOptions = [
  { 'label': 'CHRISTIANITY', 'value': 'Christianity' },
  { 'label': 'ISLAM', 'value': 'Islam' },
  { 'label': 'TRADITIONAL AFRICAN RELIGION', 'value': 'Traditional African Religion' },
  { 'label': 'HINDUISM', 'value': 'Hinduism' },
  { 'label': 'BUDDHISM', 'value': 'Buddhism' },
  { 'label': 'NONE', 'value': 'None' },
  { 'label': 'OTHER', 'value': 'Other' }
];


