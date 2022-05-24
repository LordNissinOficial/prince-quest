﻿Shader "MSLGiU/101/101a_Basic" {
  SubShader {
    Pass {
      CGPROGRAM
      #pragma vertex vert
      #pragma fragment frag

      #include "UnityCG.cginc"

      struct appdata {
        float4 vertex : POSITION;
      };
      struct v2f {
        float4 vertex : SV_POSITION;
      };

      v2f vert(appdata v) {
        v2f o;
        // does matrix multiplication on local vertex to transform it from a point on the object to a point on the screen
        o.vertex = mul(UNITY_MATRIX_MVP, v.vertex);
        return o;
      }

      float4 frag(v2f i) : SV_Target {
        // draw white pixels to the screen
        return float4(1, 1, 1, 1);
      }

      ENDCG
    }
  }
}