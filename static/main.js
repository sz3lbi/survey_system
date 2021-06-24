function calculatePoint(i, intervalSize, colorRangeInfo) {
  var { colorStart, colorEnd, useEndAsStart } = colorRangeInfo;
  return (useEndAsStart
    ? (colorEnd - (i * intervalSize))
    : (colorStart + (i * intervalSize)));
}

/* Must use an interpolated color scale, which has a range of [0, 1] */
function interpolateColors(dataLength, colorScale, colorRangeInfo) {
  var { colorStart, colorEnd } = colorRangeInfo;
  var colorRange = colorEnd - colorStart;
  var intervalSize = colorRange / dataLength;
  var i, colorPoint;
  var colorArray = [];

  for (i = 0; i < dataLength; i++) {
    colorPoint = calculatePoint(i, intervalSize, colorRangeInfo);
    colorArray.push(colorScale(colorPoint));
  }

  return colorArray;
}

function restoreFormData(postDataDict) {
  for (const [key, array] of Object.entries(postDataDict)) {
    let input;

    for (const value of array) {
      input = $(`input[name='${key}'][value='${value}']`);
      if(input.length) {
        input.prop("checked", true);
      } else {
        input = $(`input[name='${key}'][type='text']`);
        if(input.length) {
          input.val(value);
        }
      }
    }   
  }
}