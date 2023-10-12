

export default function colorWheel(number, bin){
  return 'hsl('+ (360 / bin * number )+",100%,40%)"
}