#version 330 core

uniform sampler2D tex;
uniform float time;

in vec2 uvs;
out vec4 f_color;

float rand(vec2 n) { 
    return fract(sin(dot(n, vec2(12.9898, 4.1414))) * 43758.5453);
}

float noise(vec2 p){
    return fract(sin(dot(p, vec2(12.9898,78.233))) * 43758.5453);
}

void main() {
    vec2 uv = uvs;
    

    float shake = (noise(vec2(time)) - 0.5) * 0.0009;
    uv.x += shake;
    uv.y += (noise(vec2(time * 0.5)) - 0.5) * 0.0009;
    

    vec2 offset = vec2(0.0008, 0.0008); 
    vec4 r = texture(tex, uv + offset * vec2(-1.0, 0.5) * (1.0 + sin(time)));
    vec4 g = texture(tex, uv + offset * vec2(0.0, -0.5) * (1.0 + cos(time*0.8)));
    vec4 b = texture(tex, uv + offset * vec2(1.0, 0.5) * (1.0 + sin(time*1.2)));
    

    vec3 color = vec3(r.r, g.g, b.b);
    

    float scanline = sin(uv.y * 1000.0 + time * 10.0) * 0.04;
    color += scanline;
    

    color *= 0.9 + 0.1 * rand(uv + time);
    

    vec2 vig = uv - 0.5;
    color *= 1.0 - dot(vig, vig) * 0.8;
    

    color += (noise(uv * 50.0 + time) - 0.5) * 0.08;
    
    f_color = vec4(color, g.a); 
}